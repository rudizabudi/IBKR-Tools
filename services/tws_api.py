from threading import Event, Lock, Thread
import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

from core import CoreDistributor, ReqId, tprint, RequestState

type Core = 'Core'


class TWSCon(EWrapper, EClient):
    def __init__(self):
        super().__init__()
        EClient.__init__(self, wrapper=self)

        self.core: Core = CoreDistributor.get_core()

        self.request_end: dict[str, RequestState] = {}

        self.connect(self.core.HOST_IP, self.core.API_PORT, self.core.CLIENT_ID)
        self.t: Thread = Thread(target=self.run, daemon=True)
        self.t.start()
        time.sleep(1)

    def connectAck(self):
        tprint('Connected.')
        while 'misc' not in self.core.widget_registry.keys():
            time.sleep(0.1)

        self.core.widget_registry['misc']['rightTopLabel'].setText('🟢 Connected.   ')

    def connectionClosed(self):
        tprint('Disconnected.')
        self.core.widget_registry['misc']['rightTopLabel'].setText('🔴 Not connected.   ')

    def error(self, reqId, errorCode, errorString):
        if errorCode not in (200,):
            tprint(f'{reqId}, {errorCode}, {errorString}')

        if reqId in ReqId.reqId_hashmap.keys():
            ReqId.reqId_hashmap[reqId](error=True)

    def contractDetails(self, reqId: int, contractDetails):
        #print(f'ContractDetails Callback  {contractDetails.__dict__=}')
        ReqId.reqId_hashmap[reqId](contractDetails=contractDetails)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.core.account_list = accountsList[:-1].split(',')

    def securityDefinitionOptionParameter(self, reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
        data = {'symbol': tradingClass,
                'r_expiries': expirations or [],
                'r_strikes': strikes or [],
                'r_multiplier': multiplier}

        ReqId.reqId_hashmap[reqId](**data)

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
            ReqId.reqId_hashmap[reqId](data)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        tprint(f'updatePortfolio: {contract.symbol}, {position}, {marketPrice}, {marketValue}, {averageCost}, {unrealizedPNL}, {realizedPNL}, {accountName}')

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

        self.core.bwd_raw_positions[contract['conId']] = {
            'contract': contract,
            'position': position,
            'marketPrice': marketPrice,
            'marketValue': marketValue,
            'averageCost': averageCost,
            'unrealizedPNL': unrealizedPNL,
            'realizedPNL': realizedPNL}

    def historicalData(self, reqId, bar):
        #print('HistDataInc', bar)
        if reqId not in ReqId.reqId_hashmap.keys():
            raise KeyError('ReqId not assigned to an security class instance.')

        ReqId.reqId_hashmap[reqId]({'date': bar.date, 'open': bar.open, 'high': bar.high, 'low': bar.low, 'close': bar.close})

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        super().historicalDataEnd(reqId, start, end)
        self.request_end['historicalData'] = RequestState.RECEIVED

    def accountDownloadEnd(self, accountName: str):
        super().accountDownloadEnd(accountName)
        print('accountDownloadEnd')
        if isinstance(self.core.threading_events['bwd_reqAccountUpdates'], Event) and not self.core.threading_events['bwd_reqAccountUpdates'].is_set():
            self.core.threading_events['bwd_reqAccountUpdates'].set()


class TWSConDistributor:
    _lock = Lock()
    _tws_con = None

    @classmethod
    def get_con(cls) -> TWSCon:
        if cls._tws_con is None:
            with cls._lock:
                if cls._tws_con is None:
                    cls._tws_con = TWSCon()
        return cls._tws_con




