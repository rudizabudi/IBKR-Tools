from collections import defaultdict
from datetime import datetime as dt
from ibapi.contract import Contract as ibContract
from itertools import chain
from time import sleep

from core import CoreDistributor, ReqId
from services import contracts
from services.tws_api import TWSCon, TWSConDistributor


class BXSIndexContracts:
    contracts: dict[str, None | ibContract] = {}
    active_contract: ibContract = None

    @classmethod
    def set_contract(cls, index: str, contract: ibContract):
        if index not in cls.contracts.keys():
            cls.contracts[index] = contract

    @classmethod
    def get_contract(cls, index: str) -> ibContract | None:
        if index not in cls.contracts.keys():
            return None

        return cls.contracts[index]

    @classmethod
    def get_active_contract(cls):
        return cls.active_contract


class BXSOptionChainData:
    cached_symbols = []
    expiries = defaultdict(list)
    strikes = defaultdict(list)
    multipliers = defaultdict(list)

    @classmethod
    def set_data(cls, symbol: str, r_expiries: list[float], r_strikes: list[float], r_multiplier: str):
        if symbol not in cls.cached_symbols:
            cls.cached_symbols.append(symbol)

        cls.expiries[symbol].extend(dt.strptime(x, '%Y%m%d') for x in r_expiries if x not in cls.expiries[symbol])
        cls.strikes[symbol].extend(x for x in r_strikes if x not in cls.strikes[symbol])
        cls.multipliers[symbol].extend(float(x) for x in r_multiplier.split(',') if float(x) not in cls.multipliers[symbol])


class conIdCache:
    conIDs = {}

    @classmethod
    def set_conId(cls, symbol, conId):
        cls.conIDs[symbol] = conId

    @classmethod
    def get_conId(cls, symbol) -> int:
        if symbol not in cls.conIDs.keys():
            return None
        return cls.conIDs[symbol]

def request_conId(index_contract: ibContract, con: TWSCon) -> int:

    if (conId := conIdCache.get_conId(index_contract.symbol)) is None:
        reqId = ReqId.register_reqId()

        ReqId.reqId_hashmap[reqId] = None
        con.reqContractDetails(reqId, index_contract)
        while ReqId.reqId_hashmap[reqId] is None: #TODO: Fix idling
            sleep(0.1)

        conId = ReqId.reqId_hashmap[reqId].contract.conId
        conIdCache.set_conId(index_contract.symbol, conId)

    return conId


def request_index_expiries(index_contract: ibContract):
    core = CoreDistributor.get_core()
    tws_con = TWSConDistributor.get_con()

    conId = request_conId(index_contract, tws_con)
    reqId = ReqId.register_reqId(BXSOptionChainData.set_data)

    print(f'Requesting expiries for {index_contract.symbol}')
    tws_con.reqSecDefOptParams(
            reqId=reqId,
            underlyingSymbol=index_contract.symbol,
            futFopExchange='',
            underlyingSecType='IND',
            underlyingConId=conId)

    while not any(map(lambda x: x in BXSOptionChainData.cached_symbols, index_contract.types)):
        sleep(0.1)

    core.threading_events['bxs_contract_details_received'].set()





