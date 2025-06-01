from collections import defaultdict
from datetime import datetime as dt, timedelta
from functools import partial

from ibapi.contract import Contract as ibContract
from itertools import chain
from threading import Event
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
    expiries: defaultdict[str, list[dt]] = defaultdict(list)
    strikes: defaultdict[str, list[float]] = defaultdict(list)
    multipliers: defaultdict[str, list[float]] = defaultdict(list)

    MINIMUM_FUTURE_OFFSET: int = 2  # days

    @classmethod
    def set_data(cls, symbol: str, r_expiries: tuple[float], r_strikes: tuple[float], r_multiplier: str):
        if symbol not in cls.cached_symbols:
            cls.cached_symbols.append(symbol)

        r_expiries = filter(lambda x: dt.strptime(x, '%Y%m%d') - timedelta(days=2) >= dt.now(), r_expiries)

        cls.expiries[symbol].extend(dt.strptime(x, '%Y%m%d') for x in r_expiries if x not in cls.expiries[symbol])
        cls.strikes[symbol].extend(x for x in r_strikes if x not in cls.strikes[symbol])
        cls.multipliers[symbol].extend(float(x) for x in r_multiplier.split(',') if float(x) not in cls.multipliers[symbol])


class conIdCache:
    conIDs = {}

    @classmethod
    def set_conId(cls, symbol: str, contractDetails: dict[str, ibContract | str | int | float]):
        cls.conIDs[symbol] = contractDetails.contract.conId

        core = CoreDistributor.get_core()
        if core.threading_events['reqConid']:
            core.threading_events['reqConid'].set()

    @classmethod
    def get_conId(cls, symbol: str) -> int | None:
        if symbol not in cls.conIDs.keys():
            return None
        return cls.conIDs[symbol]


def request_conId(index_contract: ibContract, con: TWSCon, core) -> int:

    if (conId := conIdCache.get_conId(index_contract.symbol)) is None:
        reqId = ReqId.register_reqId()

        conId_callback = partial(conIdCache.set_conId, symbol=index_contract.symbol)

        ReqId.reqId_hashmap[reqId] = conId_callback
        core.threading_events['reqConid'] = Event()
        con.reqContractDetails(reqId, index_contract)
        core.threading_events['reqConid'].wait()

        conId = conIdCache.get_conId(index_contract.symbol)

    return conId


def request_index_expiries(index_contract: ibContract):
    core = CoreDistributor.get_core()
    tws_con = TWSConDistributor.get_con()

    conId = request_conId(index_contract, tws_con, core)
    reqId = ReqId.register_reqId(BXSOptionChainData.set_data)

    tws_con.reqSecDefOptParams(
            reqId=reqId,
            underlyingSymbol=index_contract.symbol,
            futFopExchange='',
            underlyingSecType='IND',
            underlyingConId=conId)

    while not any(map(lambda x: x in BXSOptionChainData.cached_symbols, index_contract.types)): #TODO: Fix loop
        sleep(0.1)

    core.threading_events['bxs_contract_details_received'].set()





