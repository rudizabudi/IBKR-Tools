from collections import defaultdict
from datetime import datetime
from functools import partial
from ibapi.contract import Contract as ibContract

from PySide6.QtCore import QObject, Signal
from threading import Event

from core import ReqId, CoreDistributor
from services.tws_api import TWSConDistributor
from services.box_spread.requests_misc import BXSOptionChainData
from services.contracts import build_expiry_dummy_contract


class UpdateGuiStrikes(QObject):
    trigger_strike_update = Signal(ibContract)

    def __init__(self):
        super().__init__()

    def fire(self, current_contract: ibContract):
        self.trigger_strike_update.emit(current_contract)


class ContractExistence:
    existing_contracts = defaultdict()
    core = None

    @classmethod
    def register_contract(cls, contract: ibContract):
        cls.existing_contracts[contract] = None

    @classmethod
    def set_existence(cls, contract: ibContract, error: bool = False, register: bool = False, *args, **kwargs):
        if cls.core is None:
            cls.core = CoreDistributor.get_core()

        cls.existing_contracts[contract] = not error

        if None not in cls.existing_contracts.values() and cls.core.threading_events['check_contract_existence']:
            print('Event set')
            cls.core.threading_events['check_contract_existence'].set()

    @classmethod
    def get_valid_strikes(cls, index_contract: ibContract, expiry: datetime) -> list[datetime]:
        valid_strikes = []

        for opt_contract, is_valid in cls.existing_contracts.items():
            if not is_valid:
                continue

            symbol_con = index_contract.symbol == opt_contract.symbol
            expiry_con = expiry == datetime.strptime(opt_contract.lastTradeDateOrContractMonth, '%Y%m%d')

            if symbol_con and expiry_con:
                valid_strikes.append(float(opt_contract.strike))

        return valid_strikes

    @classmethod
    def contract_checked(cls, opt_contract: ibContract) -> bool:
        #if cls.existing_contracts.get(opt_contract, None) is not None:
        if opt_contract in cls.existing_contracts.keys():
            return True
        return False


def check_strikes(current_contract: ibContract, expiry_date: datetime, bxs_instance: "BoxSpread"):
    print('Checking for strike existence started', datetime.now(), len(ContractExistence.existing_contracts.keys()))

    tws_con = TWSConDistributor.get_con()
    core = CoreDistributor.get_core()

    core.threading_events['check_contract_existence'] = Event()
    existence_requested = False
    print(f'Len old strikes: {len(BXSOptionChainData.strikes[current_contract.selected_type])}')
    for strike in BXSOptionChainData.strikes[current_contract.selected_type]:
        opt_contract_dummy = build_expiry_dummy_contract(index_contract=current_contract,
                                                         expiry_date=expiry_date,
                                                         strike=strike)
        if ContractExistence.contract_checked(opt_contract=opt_contract_dummy):
            continue

        existence_requested = True

        price_callback = partial(ContractExistence.set_existence, contract=opt_contract_dummy)
        ContractExistence.register_contract(opt_contract_dummy)
        tws_con.reqContractDetails(ReqId.register_reqId(price_callback), opt_contract_dummy)

    if existence_requested:
        core.threading_events['check_contract_existence'].wait()

    bxs_instance.tab_trigger['strikes'].fire(current_contract)

