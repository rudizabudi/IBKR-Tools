from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading

import time

from core import tprint


class TWSCon(EWrapper, EClient):

    def __init__(self, core):

        super().__init__()
        EClient.__init__(self, wrapper=self)

        self.core = core
        self.core.no_contract = False

        self.connect(core.host_ip, core.api_port, core.client_id)
        self.t: threading.Thread = threading.Thread(target=self.run, daemon=True)
        self.t.start()
        time.sleep(1)


    def connectAck(self):
        tprint('Connected.')

    def connectionClosed(self):
        tprint('Disconnected.')

    def error(self, reqId, errorCode, errorString):
        #tprint(errorCode, errorString)
        if errorCode in [162, 200]:
            self.core.reqId_hashmap[reqId].__self__.set_error_flag(flag=True)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.core.account_list = accountsList[:-1].split(',')

    def securityDefinitionOptionParameter(self, reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
        if reqId not in self.core.reqId_hashmap.keys():
            raise KeyError('ReqId not assigned to an security class instance.')

        self.core.reqId_hashmap[reqId](expiries=list(expirations) or [], strikes=list(strikes) or [])

    def contractDetails(self, reqId: int, contractDetails):
        if reqId not in self.core.reqId_hashmap.keys():
            raise KeyError('ReqId not assigned to an security class instance.')

        self.core.reqId_hashmap[reqId](contractDetails.contract.conId)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        #tprint(f'updatePortfolio: {contract.symbol}, {position}, {marketPrice}, {marketValue}, {averageCost}, {unrealizedPNL}, {realizedPNL}, {accountName}')
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


    def tickOptionComputation(self, reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice):
        super().tickOptionComputation(reqId, tickType, tickAttrib, impliedVol, delta, optPrice, pvDividend, gamma, vega, theta, undPrice)

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

