from ibapi.contract import Contract as ibContract

from core import CoreDistributor


def create_benchmark_contract() -> ibContract:
    benchmark_contract = ibContract()
    benchmark_contract.symbol = CoreDistributor.get_core().BENCHMARK
    benchmark_contract.secType = 'STK'
    benchmark_contract.exchange = 'SMART'
    benchmark_contract.currency = 'USD'
    return benchmark_contract


def create_position_contract(**kwargs) -> ibContract:

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
