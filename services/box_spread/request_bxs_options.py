from collections import defaultdict
from datetime import datetime
from enum import StrEnum
from functools import partial
from threading import Event

from ibapi.contract import Contract as ibContract

from core import CoreDistributor, ReqId
from services.contracts import build_position_contract, build_combo_contract, add_combo_leg, ComboAction
from services.box_spread.requests_misc import request_conId
from services.box_spread.request_prices import ContractPrices
from services.tws_api import TWSConDistributor

class BoxSpreadType(StrEnum):
    LEND = 'LEND'
    BORROW = 'BORROW'


class ComboContractPrices:
    combo_prices: defaultdict[ibContract, dict[str, float]] = defaultdict(dict)

    @classmethod
    def set_price(cls, contract: ibContract, **kwargs):
        print(f'{kwargs=}')
        # cls.combo_prices[contract]['ask'] = price[0]
        # cls.combo_prices[contract]['bid'] = price[1]


def request_bxs_option_prices(index_contract: ibContract,
                              direction: BoxSpreadType,
                              expiry_date: datetime,
                              lower_strike: float,
                              upper_strike: float) -> tuple[float, float]:

    bxs_leg_actions = {
        BoxSpreadType.LEND: {
            'C': {lower_strike: ComboAction.BUY, upper_strike: ComboAction.SELL},
            'P': {lower_strike: ComboAction.SELL, upper_strike: ComboAction.BUY}
        },
        BoxSpreadType.BORROW: {
            'C': {lower_strike: ComboAction.SELL, upper_strike: ComboAction.BUY},
            'P': {lower_strike: ComboAction.BUY, upper_strike: ComboAction.SELL}
        }
    }

    bxs_combo_contract = build_combo_contract(source_contract=index_contract)
    print(41, (lower_strike, upper_strike))
    for strike in (lower_strike, upper_strike):
        for right in ('C', 'P'):
            opt_contract = build_position_contract(symbol=index_contract.symbol,
                                                   secType='OPT',
                                                   exchange=index_contract.exchange,
                                                   currency=index_contract.currency,
                                                   right=right,
                                                   strike=strike,
                                                   lastTradeDateOrContractMonth=expiry_date.strftime('%Y%m%d'))

            conId = request_conId(opt_contract)
            action = bxs_leg_actions[direction][right][strike]
            print(f'{strike=}')
            add_combo_leg(combo_contract=bxs_combo_contract,
                          conId=conId,
                          ratio=1,
                          action=action,
                          exchange=index_contract.exchange)

    print(42)
    # Request the prices for the combo contract
    core = CoreDistributor.get_core()

    comcon_price_callback = partial(ComboContractPrices.set_price, contract=bxs_combo_contract)
    reqId = ReqId.register_reqId(comcon_price_callback)

    core.threading_events['bxs_combo_request_prices'] = Event()
    print("Before bxs request")

    ContractPrices.request_price_tws(contract=bxs_combo_contract)
    print("Before bxs wait")
    core.threading_events['bxs_combo_request_prices'].wait()
    print("after bxs wait")
    #combo contract: https://interactivebrokers.github.io/tws-api/spread_contracts.html
