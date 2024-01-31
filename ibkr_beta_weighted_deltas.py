from datetime import datetime as dt
from datetime import date, timedelta
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas
import random
from tabulate import tabulate
import threading
from threading import Timer
import time
import yfinance as yf

'''**********************************************************************
* Project           : IBKR Beta Weighted Deltas
* Version           : v0.22
* 
* Date        Ref    Revision
* 20240124    v0.1      Beta
* 20240125    v0.2      Notional Positions
                        Position selection
* 20240130    v0.21     Fixed bug. Show greeks as in TWS (tickType 13)
* 20240131    v0.22     More efficient wait for callbacks to finish
**********************************************************************'''

class APIController(EWrapper, EClient):

    def _init_(self):
        EClient.__init__(self, self)
        pass

    def connectAck(self):
        print('Connected')

    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        super().tickOptionComputation(reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)
        #print((self, reqId, tickType, tickAttrib,impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice))
        if tickType == 13 and delta is not None:
            self.greek_counter += 1
            self.req_greeks[reqId] = [delta, gamma, vega, theta, impliedVol, optPrice]

    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)
        #print("Position.", "Account:", account, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency, "Position:", decimalMaxString(position), "Avg cost:", floatMaxString(avgCost))

    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        #print("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
        self.download_end = True
        #print("AccountDownloadEnd. Account:", accountName)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        # print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
        #                               "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
        #                               "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)
        contract = {'symbol': contract.symbol, 'secType': contract.secType, 'currency': contract.currency, 'right': contract.right, 'strike': contract.strike, 'lastTradeDateOrContractMonth': contract.lastTradeDateOrContractMonth}
        if position != 0:
            if contract['symbol'] in self.positions.keys():
                self.positions[contract['symbol']].append({'contract': contract, 'position': position})
            else:
                self.positions[contract['symbol']] = [{'contract': contract, 'position': position}]

    # def tickPrice(self, regId, data, oans, zwoa):
    #     print(regId)

class APISocket(EClient):

    def __init__(self, wrapper):
        super().__init__(wrapper)

class TradingApplication(APIController, APISocket):

    def __init__(self):
        self.api_port = 7497
        self.benchmark = '^SPX'
        self.beta_period = '1y' ## Valid periods: d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        self.view_selection = True

        APIController.__init__(self)
        APISocket.__init__(self, wrapper=self)
        #self.connect('127.0.0.1', 7496, 1)
        self.connect('127.0.0.1', self.api_port, 1)

        self.selected_positions = {}
        self.counter = 0
        self.download_end = False
        self.betas = {}

        self.req_greeks = {}
        self.greek_counter = 0
        self.greek_assigns = {}

        self.current_prices = {}
        time.sleep(3)

    def get_positions(self):

        self.positions = {}
        self.download_end = False
        self.reqAccountUpdates(True, "U10679162")
        t = threading.Thread(target=self.run)
        t.start()

    def position_selection(self):

        print()
        selection = -1
        if self.view_selection:
            print('Which holdings do you want data for? ')
            print(0, ': ', 'All positions')
            for i, x in enumerate(self.positions.keys(), start=1):
                print(i, ': ', x)

            while selection not in range(0, len(self.positions.keys()) + 1):
                selection = int(input('Position #: '))

            print()

        if selection == 0 or not self.view_selection:
            self.selected_positions = self.positions
        else:
            self.selected_positions[list(self.positions.keys())[selection - 1]] = self.positions[list(self.positions.keys())[selection - 1]]

    def request_delta(self):
        req_id = 0
        self.req_greeks = {}
        self.greek_assigns = {}
        for k, v in self.selected_positions.items():
            for i, x in enumerate(v, start=0):
                if x['contract']['secType'] == 'OPT' and int(date.today().strftime('%Y%m%d')) <= int(x['contract']['lastTradeDateOrContractMonth']):

                    req_contract = Contract()
                    req_contract.symbol = x['contract']['symbol']
                    req_contract.secType = x['contract']['secType']
                    req_contract.exchange = 'SMART'
                    req_contract.currency = x['contract']['currency']
                    req_contract.right = x['contract']['right']
                    req_contract.strike = float(x['contract']['strike'])
                    req_contract.lastTradeDateOrContractMonth = x['contract']['lastTradeDateOrContractMonth']

                    self.req_greeks[req_id] = []
                    self.reqMktData(req_id, req_contract, "13", True, False, [])

                    self.greek_assigns[req_id] = [k, i]
                    req_id += 1

        while not self.greek_counter == req_id:
            time.sleep(0.1)

        for i in range(req_id):
            self.selected_positions[self.greek_assigns[i][0]][self.greek_assigns[i][1]]['delta'] = self.req_greeks[i][0]

    def calculate_beta(self):
        bench_hist = yf.Ticker(self.benchmark).history(period=self.beta_period)
        bench_hist['Change'] = bench_hist['Close'].pct_change()
        variance = bench_hist['Change'].var()
        self.bench_current_price = round(bench_hist.iloc[-1]['Close'], 2)

        for k, v in self.selected_positions.items():
            stock_hist = yf.Ticker(k).history(period=self.beta_period)
            stock_hist['Change'] = stock_hist['Close'].pct_change()
            self.current_prices[k] = round(stock_hist.iloc[-1]['Close'], 2)

            covariance = stock_hist['Change'].cov(bench_hist['Change'])
            beta = covariance / variance

            self.betas[k] = beta

    def table(self):
        df = {'Underlying': [], 'Beta / Position': [], 'Amount': [], 'Delta': [], 'Beta weighted Delta': [], 'Notional Position': []}
        beta_list = []
        delta_list = []
        bwd_list = []
        np_list = []
        for k, v in self.betas.items():
            df['Underlying'].append(k)
            df['Beta / Position'].append(round(v, 2))
            beta_list.append(round(v, 2))
            df['Amount'].append('')
            df['Delta'].append('')
            df['Beta weighted Delta'].append('')
            df['Notional Position'].append('')

            beta = v
            for y in self.selected_positions[k]:
                df['Underlying'].append('')
                if y['contract']['secType'] == 'OPT':
                    name = str(y['contract']['strike']) + ' ' + ('Call' if y['contract']['right'] == 'C' else 'Put') + ' ' + dt.strptime(y['contract']['lastTradeDateOrContractMonth'], '%Y%m%d').strftime('%d%b%y')
                elif y['contract']['secType'] == 'STK':
                    name = k + ' ' + 'Stock'
                df['Beta / Position'].append(name)

                amount = y['position']
                df['Amount'].append(amount)

                if y['contract']['secType'] == 'OPT':
                    try:
                        delta = y['delta'] * amount * 100 #TODO: implement options other than multiplicator == 100
                    except KeyError:
                        print(y)
                        print( )
                        print(self.selected_positions)
                        print('- - - ')
                        exit()
                elif y['contract']['secType'] == 'STK':
                    delta = amount
                df['Delta'].append(round(delta, 2))
                delta_list.append(round(delta, 2))

                bwd = beta * delta
                df['Beta weighted Delta'].append(round(bwd, 2))
                bwd_list.append(round(bwd, 2))

                df['Notional Position'].append(round((self.current_prices[k] * bwd), 2))
                np_list.append(round((self.current_prices[k] * bwd), 2))

            df['Underlying'].append('')
            df['Beta / Position'].append('')
            df['Amount'].append('')
            df['Delta'].append('')
            df['Beta weighted Delta'].append('')
            df['Notional Position'].append('')

        df['Underlying'].append('TOTAL')
        df['Beta / Position'].append(round(sum(beta_list), 2))
        df['Amount'].append('')
        df['Delta'].append(round(sum(delta_list), 2))

        for i, x in enumerate(df['Delta']):
            if df['Delta'][i] == '' and df['Delta'][min(i + 1, len(df['Delta']) - 2)] != '':
                total = 0
                for y in df['Delta'][i + 1:len(df['Delta']) - 1]:
                    if isinstance(y, (int, float)):
                        total += y
                    else:
                        break
                df['Delta'][i] = round(total, 2)

        df['Beta weighted Delta'].append(round(sum(bwd_list), 2))
        for i, x in enumerate(df['Beta weighted Delta']):
            if df['Beta weighted Delta'][i] == '' and df['Beta weighted Delta'][min(i + 1, len(df['Beta weighted Delta']) - 2)] != '':
                total = 0
                for y in df['Beta weighted Delta'][i + 1:len(df['Beta weighted Delta']) - 1]:
                    if isinstance(y, (int, float)):
                        total += y
                    else:
                        break
                df['Beta weighted Delta'][i] = round(total, 2)

        df['Notional Position'].append(round(sum(np_list), 2))
        for i, x in enumerate(df['Delta']):
            if df['Notional Position'][i] == '' and df['Notional Position'][min(i + 1, len(df['Notional Position']) - 2)] != '':
                total = 0
                for y in df['Notional Position'][i + 1:len(df['Notional Position']) - 1]:
                    if isinstance(y, (int, float)):
                        total += y
                    else:
                        break
                df['Notional Position'][i] = round(total, 2)

        df = pandas.DataFrame(df)
        #print('Notional value based on', self.bench_current_price, 'benchmark.')
        print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=('.2f'), numalign='right', stralign='right', showindex=False))

    def main(self):
        self.get_positions()
        while not self.download_end:
            time.sleep(0.1)
        self.download_end = False

        self.position_selection()

        self.request_delta()

        self.calculate_beta()

        self.table()


TradingApplication().main()

