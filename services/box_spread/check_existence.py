from collections import defaultdict
from datetime import datetime
from functools import partial
from ibapi.contract import Contract as ibContract

from PySide6.QtCore import QObject, Signal
from threading import Event

from core import ReqId, CoreDistributor
from services.tws_api import TWSConDistributor
from services.box_spread.request_expiries import BXSOptionChainData
from services.contracts import create_expiry_dummy_contract


class UpdateGuiStrikes(QObject):
    trigger_strike_update = Signal(list)

    def __init__(self):
        super().__init__()

    def start(self, current_contract, expiry_date):
        data = ContractExistence.get_valid_strikes(current_contract, expiry_date)
        self.trigger_strike_update.emit(data)


class ContractExistence():
    existing_contracts = defaultdict(bool)
    core = None

    @classmethod
    def set_existence(cls, contract: ibContract, error: bool = False, *args, **kwargs):
        if cls.core is None:
            cls.core = CoreDistributor.get_core()

        if error:
            cls.existing_contracts[contract] = False
        else:
            cls.existing_contracts[contract] = True

        if cls.core.threading_events['check_contract_existence']:
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
    def get_validity_status(cls, opt_contract: ibContract, strike: float) -> bool:
        if cls.existing_contracts[opt_contract]:
            return True
        return False


def check_strikes(current_contract: ibContract, expiry_date: datetime, bxs_instance: "BoxSpread"):
    tws_con = TWSConDistributor.get_con()
    core = CoreDistributor.get_core()
    tab_trigger = bxs_instance.tab_trigger['strikes']

    for strike in BXSOptionChainData.strikes[current_contract.symbol]:
        opt_contract_dummy = create_expiry_dummy_contract(index_contract=current_contract,
                                                             expiry_date=expiry_date,
                                                             strike=strike)

        if ContractExistence.get_validity_status(opt_contract=opt_contract_dummy, strike=strike):
            continue

        price_callback = partial(ContractExistence.set_existence, contract=opt_contract_dummy)

        core.threading_events['check_contract_existence'] = Event()
        tws_con.reqContractDetails(ReqId.register_reqId(price_callback), opt_contract_dummy)
        core.threading_events['check_contract_existence'].wait()

    tab_trigger.start(current_contract, expiry_date)
    #ContractExistence.gui_update_strikes(current_contract, expiry_date)

    # strikes = ContractExistence.get_valid_strikes(current_contract, expiry_date)
    # print('Existence checked')
    # bxs_instance.set_strike_comboBoxes(current_contract, strikes)
    # print('Strikes updated')
