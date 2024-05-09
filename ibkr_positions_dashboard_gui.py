from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QScrollArea,
    QTableWidget,
    QWidget,
    QHBoxLayout,
    QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QSizePolicy, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QPalette, QColor, QResizeEvent, QFont
import threading

from datetime import datetime as dt
from datetime import date, timedelta
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import time
import yfinance as yf

'''**********************************************************************
* Project           : IBKR Positions Dashboard GUI
* Version           : v0.21
* 
* Date        Ref    Revision
* 20240417    v0.1   Alpha
* 20240505    v0.2   iVol, theta, gamma added & cosmetics
**********************************************************************'''

class APIController(EWrapper, EClient):

    def _init_(self):
        EClient.__init__(self, self)
        pass

    def connectAck(self):
        print('Connected')

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.accountsList = accountsList[:-1].split(',')
        #print("Account list:", accountsList)

    def accountSummary(self, reqId, account, tag, value, currency):
        super().accountSummary(reqId, account, tag, value, currency)
        #print("AccountSummary. ReqId:", reqId, "Account:", account,"Tag: ", tag, "Value:", value, "Currency:", currency)

    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        super().tickOptionComputation(reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)
        #print(reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)

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

        self.position_download_end = True
        #print("AccountDownloadEnd. Account:", accountName)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        # print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
        #                               "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
        #                               "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)
        contract = {'symbol': contract.symbol, 'secType': contract.secType, 'currency': contract.currency, 'right': contract.right, 'strike': contract.strike, 'lastTradeDateOrContractMonth': contract.lastTradeDateOrContractMonth}
        if position != 0:
            if contract['symbol'] in positions.keys():
                positions[contract['symbol']].append({'contract': contract, 'position': position})
            else:
                positions[contract['symbol']] = [{'contract': contract, 'position': position}]

    # def tickPrice(self, regId, data, oans, zwoa):
    #     print(regId)

class APISocket(EClient):
    def __init__(self, wrapper):
        super().__init__(wrapper)

class TradingApplication(APIController, APISocket):

    def __init__(self):
        self.api_port = 7497
        self.benchmark = '^SPX'
        self.beta_period = '1y' # Valid periods: d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        self.acctCode = 0 # selected subacount by alphanumerical order. Start = 0

        APIController.__init__(self)
        APISocket.__init__(self, wrapper=self)
        self.connect('127.0.0.1', self.api_port, 1337)

        self.accountsList = []
        self.req_id = 0
        self.pos_greeks = {}
        self.position_download_end = False
        self.betas = {}

        self.req_greeks = {}
        self.greek_counter = 0
        self.greek_assigns = {}

        self.current_prices = {}
        self.t = threading.Thread(target=self.run)
        self.t.start()
        time.sleep(3)

    def terminate_connection(self):
        #self.disconnect()
        self.t.join()
    def get_positions(self):
        self.position_download_end = False
        global positions
        positions = {}
        time.sleep(1)
        self.reqManagedAccts()
        while not self.accountsList:
            time.sleep(0.1)

        #self.reqAccountSummary(1337, "All", account_summary_tags.AccountSummaryTags.AllTags)
        self.reqAccountUpdates(True, self.accountsList[self.acctCode])
        while not self.position_download_end:
            time.sleep(0.1)

        self.reqAccountUpdates(False, self.accountsList[self.acctCode])

        return positions
    def request_delta(self):
        #self.reqIds(-1)

        self.req_greeks = {}
        self.greek_assigns = {}
        # print('PositionsRequestDelta:', positions)
        for k, v in positions.items():
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
                    self.req_greeks[self.req_id] = []
                    self.reqMktData(self.req_id, req_contract, '13', True, False, [])

                    while self.req_id not in self.req_greeks.keys():
                        time.sleep(0.5)

                    self.greek_assigns[self.req_id] = [k, i]
                    self.req_id += 1

        time.sleep(5)
        self.greek_counter = 0

        greeks_received = False
        while not greeks_received:
            try:
                for i in list(self.greek_assigns.keys()):
                    positions[self.greek_assigns[i][0]][self.greek_assigns[i][1]]['delta'] = self.req_greeks[i][0]
                    positions[self.greek_assigns[i][0]][self.greek_assigns[i][1]]['gamma'] = self.req_greeks[i][1]
                    positions[self.greek_assigns[i][0]][self.greek_assigns[i][1]]['theta'] = self.req_greeks[i][3]
                    positions[self.greek_assigns[i][0]][self.greek_assigns[i][1]]['ivol'] = self.req_greeks[i][4]
                    greeks_received = True
            except IndexError:
                print('Index Error i:', i)
                print('Greek_Assigns:', self.greek_assigns)
                print('Req-Greeks:', self.req_greeks)
                print(' - - - ')
                time.sleep(10)

        last_update = dt.now().strftime('%H:%M')
    def calculate_beta(self):
        beta_received = False
        while not beta_received:
            try:
                bench_hist = yf.Ticker(self.benchmark).history(period=self.beta_period)
                bench_hist['Change'] = bench_hist['Close'].pct_change()
                variance = bench_hist['Change'].var()
                self.bench_current_price = round(bench_hist.iloc[-1]['Close'], 2)

                for k, v in positions.items():
                    if k not in self.betas.keys():
                        stock_hist = yf.Ticker(k).history(period=self.beta_period)
                        stock_hist['Change'] = stock_hist['Close'].pct_change()
                        self.current_prices[k] = round(stock_hist.iloc[-1]['Close'], 2)

                        covariance = stock_hist['Change'].cov(bench_hist['Change'])
                        beta = covariance / variance

                        self.betas[k] = beta
                beta_received = True

            except ValueError:
                continue

    def table(self):
        df = {'Underlying': [], 'Beta / Position': [], 'Amount': [], 'iVol': [], 'Delta': [], 'Beta weighted Delta': [], 'Theta': [], 'Gamma': [], 'Notional Position': []}
        beta_list = []
        ivol_list = []
        delta_list = []
        bwd_list = []
        theta_list = []
        gamma_list = []
        np_list = []

        if not list_selection in ['Portfolio', 'Overview']:
            table_betas = {list_selection: self.betas[list_selection]}
        else:
            table_betas = self.betas

        #try:
        for k, v in table_betas.items():
            df['Underlying'].append(k)
            df['Beta / Position'].append(round(v, 2))
            beta_list.append(round(v, 2))
            df['Amount'].append('')
            df['iVol'].append('')
            df['Delta'].append('')
            df['Beta weighted Delta'].append('')
            df['Theta'].append('')
            df['Gamma'].append('')
            df['Notional Position'].append('')

            beta = v
            for y in positions[k]:
                df['Underlying'].append('')
                if y['contract']['secType'] == 'OPT':
                    name = str(y['contract']['strike']) + ' ' + ('Call' if y['contract']['right'] == 'C' else 'Put') + ' ' + dt.strptime(y['contract']['lastTradeDateOrContractMonth'], '%Y%m%d').strftime('%d%b%y')
                elif y['contract']['secType'] == 'STK':
                    name = k + ' ' + 'Stock'
                elif y['contract']['secType'] == 'FUT':
                    name = k + ' ' + 'Future'
                df['Beta / Position'].append(name)

                amount = y['position']
                df['Amount'].append(amount)

                ivol = round(y['ivol'], 2) if y['contract']['secType'] == 'OPT' else 0
                df['iVol'].append(ivol)
                ivol_list.append(ivol)

                if y['contract']['secType'] == 'OPT':
                    delta = y['delta'] * amount * 100 #TODO: implement options other than multiplicator == 100
                elif y['contract']['secType'] == 'STK':
                    delta = amount

                df['Delta'].append(round(delta, 2))
                delta_list.append(round(delta, 2))

                bwd = beta * delta
                df['Beta weighted Delta'].append(round(bwd, 2))
                bwd_list.append(round(bwd, 2))

                theta = round(y['theta'] * amount * 100, 2) if y['contract']['secType'] == 'OPT' else 0
                df['Theta'].append(theta)
                theta_list.append(theta)

                gamma = round(y['gamma'] * amount * 100, 2) if y['contract']['secType'] == 'OPT' else 0
                df['Gamma'].append(gamma)
                gamma_list.append(gamma)

                #df['Notional Position'].append(round((self.current_prices[k] * bwd), 2))
                df['Notional Position'].append(round((self.current_prices[k] * delta), 2))

                np_list.append(round((self.current_prices[k] * bwd), 2))

            df['Underlying'].append('')
            df['Beta / Position'].append('')
            df['Amount'].append('')
            df['iVol'].append('')
            df['Delta'].append('')
            df['Beta weighted Delta'].append('')
            df['Theta'].append('')
            df['Gamma'].append('')
            df['Notional Position'].append('')

        df['Underlying'].append('TOTAL')
        df['Beta / Position'].append(round(sum(beta_list), 2))
        df['Amount'].append('')

        categories = {'iVol': ivol_list,
                      'Delta': delta_list,
                      'Beta weighted Delta': bwd_list,
                      'Theta': theta_list,
                      'Gamma': gamma_list,
                      'Notional Position': np_list}

        for k, v in categories.items():
            df[k].append(round(sum(v), 2))
            for i, x in enumerate(df[k]):
                if df[k][i] == '' and df[k][min(i + 1, len(df[k]) - 2)] != '':
                    total = 0
                    gamma_l = 0
                    gamma_s = 0
                    ivol_list = []
                    for y in range(i + 1, len(df[k])):
                        if k == 'Gamma':
                            if ((' Call ' in str(df['Beta / Position'][y]) and df['Amount'][y] > 0) or (' Put ' in str(df['Beta / Position'][y]) and df['Amount'][y] < 0)) and isinstance(y, (int, float)): #bullish
                                total += df[k][y]
                                gamma_l += df[k][y]
                            elif ((' Call ' in str(df['Beta / Position'][y]) and df['Amount'][y] < 0) or (' Put ' in str(df['Beta / Position'][y]) and df['Amount'][y] > 0)) and isinstance(y, (int, float)): #bearish
                                total += df[k][y]
                                gamma_s += df[k][y]
                            elif not isinstance(df[k][y], (int, float)):
                                total = str(round(gamma_l, 5)) + ' | ' + str(round(gamma_s, 5))
                                break
                        elif k == 'iVol':
                            if isinstance(df[k][y], (int, float)):
                                ivol_list.append(df[k][y])
                            else:
                                total = sum(ivol_list) / len(ivol_list)
                                break
                        else:
                            if isinstance(df[k][y], (int, float)):
                                total += df[k][y]
                            else:
                                total = round(total, 2)
                                break
                    df[k][i] = total

        for i, x in enumerate(df['iVol']):
            if isinstance(x, (int, float)):
                df['iVol'][i] = str(int(x * 100)) + '%'
        return df
        #df.to_csv('bwd_df_dummy.csv', index=False)

        # except KeyError as e:
        #     print(e)
        #     return
class gui_thread(QMainWindow):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def resizeEvent(self, event: QResizeEvent):
        column_ratios = {0: 4,
                         1: 7,
                         2: 2,
                         3: 3,
                         4: 4,
                         5: 7,
                         6: 4,
                         7: 5,
                         8: 6}

        for k, v in column_ratios.items():
            width = int(round((bwd_table.width() / sum(column_ratios.values())) * v * .98, 0))
            bwd_table.setColumnWidth(k, width)

    def create_gui(self):

        self.setWindowTitle("IBKR Tools - Beta weighted deltas")
        self.setGeometry(25, 40, 1250, 1250)  # Set window position and size

        global list_widget
        list_widget = QListWidget()
        list_widget.setFixedSize(200, 1245)
        list_widget.setFont(QFont("", 18))

        list_widget.currentItemChanged.connect(self.handle_list_selection)

        global bwd_table
        bwd_table = QTableWidget(1000, 9)
        bwd_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bwd_table.setMinimumSize(1020, 1230)
        headers = ['Underlying', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', ' γ Gamma (L|S)', 'Notional position']
        bwd_table.setHorizontalHeaderLabels(headers)

        bwd_table.setSelectionMode(QAbstractItemView.NoSelection)
        bwd_table.verticalHeader().setVisible(False)
        #bwd_table.setFixedSize(800, 960)
        #bwd_table.setMinimumWidth(800)

        l1_box = QHBoxLayout()
        l1_box.setAlignment(Qt.AlignLeft)
        l1_box.addWidget(list_widget)
        l2_box = QVBoxLayout()
        l2_box.setAlignment(Qt.AlignCenter)
        l2_box.setStretch(1, 1)

        l3_box = QHBoxLayout()
        l3_box.setAlignment(Qt.AlignCenter)

        refresh_button = QPushButton("Refresh")
        refresh_button.setFixedWidth(300)

        l4_box = QHBoxLayout()
        l4_box.setAlignment(Qt.AlignRight)

        global refresh_label
        refresh_label = QLabel()
        #refresh_label.setStyleSheet("text-align: right;")
        l4_box.addStretch()
        l4_box.addWidget(refresh_label)

        l3_box.addWidget(refresh_button)
        l3_box.addLayout(l4_box)
        l2_box.addLayout(l3_box)
        l2_box.addWidget(bwd_table)

        l1_box.addLayout(l2_box)
        central_widget = QWidget()
        central_widget.setLayout(l1_box)

        # Set the central widget
        self.setCentralWidget(central_widget)
    def change_table(self, df):
        bwd_table.clear()

        print('Change Table Current selection:', list_selection)
        if list_selection == 'Overview':
            df_ls = {}
            print('Overview triggered')
            for i, x in enumerate(df['Underlying']):
                if not (df['Underlying'][i] == '' and df['Beta / Position'][i] != ''):
                    for y in ['Underlying', 'Beta / Position', 'Amount', 'iVol', 'Delta', 'Beta weighted Delta', 'Theta', 'Gamma', 'Notional Position']:
                        if y not in df_ls.keys():
                            df_ls[y] = [df[y][i]]
                        else:
                            df_ls[y].append(df[y][i])

            df = df_ls

        for i, x in enumerate(df.keys()): # columns
            for j, y in enumerate(df[x]): # rows
                if i not in [0, 1, 2] and isinstance(y, (int, float)):
                    y = f'{y:.2f}'
                item = QTableWidgetItem(str(y))
                if i in [8]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif i in [1, 2, 3, 4, 5, 6, 7,]:
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

                #if list_selection !='Overview' or (list_selection =='Overview' and (df[list(df.keys())[0]][i] == df[list(df.keys())[1]][i] or df[list(df.keys())[1]][i] != '')):
                bwd_table.setItem(j, i, item)
                    #item.setForeground(QtGui.QBrush(QtGui.QColor(0, 128, 0)))

        headers = ['Underlying', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', 'γ Gamma (L|S)', 'Notional position']
        bwd_table.setHorizontalHeaderLabels(headers)
        bwd_table.viewport().update()

        last_update = dt.now().strftime('%H:%M')
        refresh_label.setText(f"{'Last update: ':>20}{last_update}")

    def change_list(self, positions):
        list_widget.clear()
        list_items = ['Portfolio', 'Overview']
        for x in positions.keys():
            list_items.append(str(x))
        list_widget.addItems(list_items)

        #print(list_selection)
        list_order = {}
        for x in range(list_widget.count()):
            list_order[list_widget.item(x).text()] = x

        if list_selection is not None:
            list_widget.setCurrentRow(list_order[list_selection])
        elif old_selection is not None:
            list_widget.setCurrentRow(list_order[old_selection])
        else:
            list_widget.setCurrentRow(0)

        list_widget.viewport().update()

    def handle_list_selection(self, current_item):
        global list_selection
        #print('Start Handle List Current selection:', list_selection)
        #print('Start Handle List Old selection:', old_selection)

        if current_item is None:
            list_selection = old_selection
        else:
            list_selection = current_item.text()

        #print('End Handle List Current selection:', list_selection)
        #print('End Handle List Old selection:', old_selection)

def set_skin(app):
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130,
                                                218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    return app

if __name__ == "__main__":
    def gui():
        global app
        app = QApplication([])
        app = set_skin(app)
        window = gui_thread()
        window.create_gui()
        window.show()
        app.exec_()

    threading.Thread(target=gui).start()

    global list_selection
    list_selection = 'Overview'
    global last_update
    last_update = ''

    def main_loop():
        ta = TradingApplication()
        loop_time = 60
        while True:
            positions = ta.get_positions()
            gui_thread().change_list(positions)

            ta.request_delta()
            ta.calculate_beta()

            df = ta.table()
            gui_thread().change_table(df)

            global old_selection
            old_selection = list_selection
            counter = 0
            while counter <= loop_time:
                time.sleep(1)
                counter += 1
                if old_selection != list_selection:
                    df = ta.table()
                    gui_thread().change_table(df)
                    old_selection = list_selection

    main_loop()





