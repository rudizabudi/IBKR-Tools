import threading
import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

from core import Core, CoreDistributor
from core import tprint


class TWSCon(EWrapper, EClient):

    def __init__(self):

        super().__init__()
        EClient.__init__(self, wrapper=self)

        self.core: Core = CoreDistributor.get_core()
        self.core.no_contract = False
        self.connect(self.core.HOST_IP, self.core.API_PORT, self.core.CLIENT_ID)
        self.t: threading.Thread = threading.Thread(target=self.run, daemon=True)
        self.t.start()
        time.sleep(1)

    def connectAck(self):
        tprint('Connected.')

    def connectionClosed(self):
        tprint('Disconnected.')

    def error(self, reqId, errorCode, errorString):
        #tprint(f'{reqId}, {errorCode}, {errorString}')
        if errorCode in [162, 200]:
            self.core.reqId_hashmap[reqId].__self__.set_error_flag(flag=True)

    def contractDetails(self, reqId: int, contractDetails):
        if reqId not in self.core.reqId_hashmap.keys():
            raise KeyError('ReqId not assigned to an security class instance.')

        self.core.reqId_hashmap[reqId](contractDetails.contract.conId)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.core.account_list = accountsList[:-1].split(',')

    def securityDefinitionOptionParameter(self, reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
        if reqId not in self.core.reqId_hashmap.keys():
            raise KeyError('ReqId not assigned to an security class instance.')

        self.core.reqId_hashmap[reqId](expiries=list(expirations) or [], strikes=list(strikes) or [])

    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        super().tickOptionComputation(reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)
        #print('Greeks received')
        if tickType == 13 and delta is not None:
            data = {
                'delta': delta,
                'gamma': gamma,
                'theta': theta,
                'vega': vega,
                'iVol': impliedVol,
                'optPrice': optPrice,
                'undPrice': undPrice
            }
            self.core.reqId_hashmap[reqId](data)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        #tprint(f'updatePortfolio: {contract.symbol}, {position}, {marketPrice}, {marketValue}, {averageCost}, {unrealizedPNL}, {realizedPNL}, {accountName}')

        # for x in dir(contract):
        #     tprint(f'{x}: {getattr(contract, x)}')
        # tprint(' - - - ')

        contract = {'symbol': contract.symbol,
                    'secType': contract.secType,
                    'currency': contract.currency,
                    'right': contract.right,
                    'strike': contract.strike,
                    'lastTradeDateOrContractMonth': contract.lastTradeDateOrContractMonth,
                    'conId': contract.conId}

        self.core.raw_positions[contract['conId']] = {
            'contract': contract,
            'position': position,
            'marketPrice': marketPrice,
            'marketValue': marketValue,
            'averageCost': averageCost,
            'unrealizedPNL': unrealizedPNL,
            'realizedPNL': realizedPNL}

    def historicalData(self, reqId, bar):
        #print('HistDataInc', bar)
        if reqId not in self.core.reqId_hashmap.keys():
            raise KeyError('ReqId not assigned to an security class instance.')

        self.core.reqId_hashmap[reqId]({bar.date: {'Open': bar.open, 'High': bar.high, 'Low': bar.low, 'Close': bar.close}})

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.core.reqId_hashmap[reqId].__self__.set_historical_data_end(flag=True)

    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print("AccountDownloadEnd. Account:", accountName)
        self.core.requesting_positions = False




