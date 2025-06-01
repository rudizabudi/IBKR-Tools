from collections import defaultdict
from datetime import datetime
from functools import partial
from threading import Event

from ibapi.contract import Contract as ibContract

from core import CoreDistributor, ReqId
from services.contracts import create_position_contract
from services.tws_api import TWSConDistributor


class conIdCache:
    conIDs = defaultdict(int)

    @classmethod
    def set_conId(cls, contract: ibContract, conId: int):
        cls.conIDs[contract] = conId

        core = CoreDistributor.get_core()
        if core.threading_events['reqConid']:
            core.threading_events['reqConid'].set()

    @classmethod
    def get_conId(cls, contract: ibContract) -> int:
        if contract not in cls.conIDs.keys():
            return None
        return cls.conIDs[contract]

def request_bxs_option_prices(index_contract: ibContract, expiry_date: datetime, lower_strike: float, upper_strike: float) -> dict:

    print(98798, index_contract, expiry_date, lower_strike, upper_strike)

    bxs_single_contracts = []
    for strike in (lower_strike, upper_strike):
        for right in ('C', 'P'):
            opt_contract = create_position_contract(symbol=index_contract.symbol,
                                                    secType='OPT',
                                                    exchange='SMART',
                                                    currency=index_contract.currency,
                                                    right=right,
                                                    strike=strike,
                                                    lastTradeDateOrContractMonth=expiry_date.strftime('%Y%m%d'))
            bxs_single_contracts.append(opt_contract)

    core = CoreDistributor.get_core()
    con = TWSConDistributor.get_con()
    for bxs_contract in bxs_single_contracts:
        if (conId := conIdCache.get_conId(bxs_contract)) is None:
            conId_callback = partial(conIdCache.set_conId, contract=bxs_contract)

            reqId = ReqId.register_reqId(conId_callback)

            ReqId.reqId_hashmap[reqId] = conId_callback
            core.threading_events['reqConid'] = Event()
            con.reqContractDetails(reqId, index_contract)
            core.threading_events['reqConid'].wait()

            conId = conIdCache.get_conId(index_contract.symbol)
            continue

        bxs_contract.conId = conId
    print(2345, bxs_single_contracts)


    #combo contract: https://interactivebrokers.github.io/tws-api/spread_contracts.html
