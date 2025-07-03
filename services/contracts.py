from datetime import datetime, timedelta
from enum import StrEnum

from ibapi.contract import Contract as ibContract, ComboLeg

from core import CoreDistributor


class ibContractCustomization:
    def __eq__(self, other):
        if not isinstance(other, ibContract):
            return False

        self_combo_legs = frozenset(self.comboLegs) if isinstance(self.comboLegs, list) else ''
        other_combo_legs = frozenset(other.comboLegs) if isinstance(other.comboLegs, list) else ''

        return (self.symbol == other.symbol and
                self.secType == other.secType and
                self.exchange == other.exchange and
                self.currency == other.currency and
                self.right == other.right and
                self.strike == other.strike and
                self.lastTradeDateOrContractMonth == other.lastTradeDateOrContractMonth and
                self_combo_legs == other_combo_legs)

    def __hash__(self):
        self_combo_legs = frozenset(self.comboLegs) if isinstance(self.comboLegs, list) else ''

        return hash((self.symbol, self.secType, self.exchange, self.currency,
                     self.right, self.strike, self.lastTradeDateOrContractMonth,
                     self_combo_legs))


ibContract.__eq__ = ibContractCustomization.__eq__
ibContract.__hash__ = ibContractCustomization.__hash__


class ComboLegCustomization:
    def __eq__(self, other):
        if not isinstance(other, ComboLeg):
            return False

        return (self.conId == other.conId and
                self.ratio == other.ratio and
                self.action == other.action and
                self.exchange == other.exchange)

    def __hash__(self):
        return hash((self.conId, self.ratio, self.action, self.exchange))


ComboLeg.__eq__ = ComboLegCustomization.__eq__
ComboLeg.__hash__ = ComboLegCustomization.__hash__

def build_benchmark_contract() -> ibContract:
    benchmark_contract = ibContract()
    benchmark_contract.symbol = CoreDistributor.get_core().settings['beta_weighted_deltas']['beta_benchmark']
    benchmark_contract.secType = 'STK'
    benchmark_contract.exchange = 'SMART'
    benchmark_contract.currency = 'USD'

    return benchmark_contract


def build_position_contract(**kwargs) -> ibContract:

    stk = all(x in kwargs.keys() for x in ('symbol', 'secType', 'currency'))
    opt = stk and all(x in kwargs.keys() for x in ('right', 'strike', 'lastTradeDateOrContractMonth'))

    if not stk and not opt:
        raise Exception('Provided arguments not sufficient to build a contract', kwargs, stk, opt)

    contract = ibContract()
    contract.symbol = kwargs['symbol']
    contract.secType = kwargs['secType']
    contract.exchange = kwargs.get('exchange', 'SMART')
    contract.currency = kwargs['currency']

    if opt:
        contract.right = kwargs['right']
        contract.strike = float(kwargs['strike'])
        contract.lastTradeDateOrContractMonth = kwargs['lastTradeDateOrContractMonth']
        # if kwargs['contract']['secType'] == 'FOP':
        #     self.contract.multiplier = "50"

    return contract


def build_index_contract(data: dict[str, str], json_data: dict) -> ibContract:
    contract = ibContract()
    contract.symbol = json_data['currencies'][data['currency']][data['index']]['symbol']
    contract.secType = 'IND'
    contract.exchange = json_data['currencies'][data['currency']][data['index']]['exchange']
    contract.currency = data['currency']
    contract.types = json_data['currencies'][data['currency']][data['index']]['types']
    contract.yf_symbol = json_data['currencies'][data['currency']][data['index']]['yf_symbol']
    contract.selected_type = None

    return contract


def build_expiry_dummy_contract(index_contract: ibContract, expiry_date: datetime, strike: float) -> ibContract:

    contract = ibContract()
    contract.symbol = index_contract.symbol
    contract.secType = 'OPT'
    contract.exchange = index_contract.exchange
    contract.currency = index_contract.currency
    contract.strike = strike
    contract.right = 'C'
    contract.lastTradeDateOrContractMonth = expiry_date.strftime('%Y%m%d')

    return contract


def build_combo_contract(source_contract: ibContract) -> ibContract:
    combo_contract = ibContract()
    combo_contract.symbol = source_contract.symbol
    combo_contract.secType = 'BAG'
    combo_contract.exchange = source_contract.exchange
    combo_contract.currency = source_contract.currency

    return combo_contract


class ComboAction(StrEnum):
    BUY = 'BUY'
    SELL = 'SELL'


def add_combo_leg(combo_contract: ibContract, conId: int, ratio: int, action: ComboAction, exchange: str) -> ibContract:

    leg = ComboLeg()
    leg.conId = conId
    leg.ratio = ratio
    leg.action = action.value
    leg.exchange = exchange

    if combo_contract.comboLegs is None:
        combo_contract.comboLegs = []
    print(f'{leg=}')
    combo_contract.comboLegs.append(leg)

    return combo_contract


