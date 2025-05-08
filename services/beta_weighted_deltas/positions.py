from datetime import datetime

from ibapi.contract import Contract as ibContract

from core import Core, CoreDistributor
from services.beta_weighted_deltas.contracts import create_benchmark_contract, create_position_contract


class Position:
    def __init__(self, benchmark: bool = False, **kwargs):
        self.core: Core = CoreDistributor.get_core()

        if benchmark:
            self.contract: ibContract = create_benchmark_contract()
        else:
            self.contract: ibContract = create_position_contract(**kwargs['contract'])

        self.symbol: str = self.contract.symbol
        self.qty: int | float = kwargs.get('position', 0.0)
        self.market_price: int | float = kwargs.get('marketPrice', 0.0)

        self.greeks = {}
        self.price_data = {}
        self.historical_data_end = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return Exception('Cannot compare Position instance with other class instance.')

        return self.contract == other.contract and self.qty == other.qty

    def __hash__(self) -> int:
        return hash((self.contract, self.qty))

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        match self.contract.secType:
            case 'STK':
                return f'<Data Container Instance> {self.contract.symbol} {self.contract.secType} & PosSize {self.qty}'
            case 'OPT':
                dt_s: str = datetime.strptime(self.contract.lastTradeDateOrContractMonth, "%Y%m%d").strftime("%d%b%y")
                return f'<Data Container Instance> {self.contract.symbol} {self.contract.strike}{self.contract.right} {dt_s} {self.contract.secType} & PosSize {self.qty}'
            case _:
                raise Exception(f'Contract type {self.contract.secType} not supported.')

    def generate_name(self) -> str:
        match self.contract.secType:
            case 'STK':
                return f'{self.contract.symbol} Stock'
            case 'OPT' | 'FOP':
                return f'{self.contract.strike} {'Call' if self.contract.right == 'C' else 'Put'} {self.get_expiry(output_str_format='%d%b%y')}'
            case _:
                raise Exception(f'Contract type {self.contract.secType} not supported.')

    def get_contract(self) -> ibContract:
        return self.contract

    def get_currency(self) -> str:
        return self.contract.currency

    def get_expiry(self, dt_object: bool = False, output_str_format: str = '%Y%m%d', ** kwargs) -> datetime | str | None:
        if self.contract.secType not in ('OPT', 'FOP'):
            raise Exception(f'Expiry date only available for contract instances of secType OPT. Requested {self.contract.symbol} of type {self.contract.secType}.')
        dt = datetime.strptime(self.contract.lastTradeDateOrContractMonth, '%Y%m%d')
        if dt_object:
            return dt
        else:
            return dt.strftime(output_str_format)

    def get_greeks(self) -> dict[str, float]:
        return self.greeks

    def get_identifier(self) -> dict[str, int | float | str]:
        return {'name': self.generate_name(), 'pos': self.qty}

    def get_qty(self) -> int | float:
        return self.qty

    def get_price(self) -> float:
        return self.market_price

    def get_secType(self) -> str:
        return self.contract.secType

    def get_symbol(self) -> str:
        return self.symbol

    def set_error_flag(self, flag: bool = False, **kwargs):
        print(f'Error flag {flag}')
        self.error_flag = flag

    def set_greeks(self, greeks: dict):
        #print(f'Set greeks {greeks} for {self.symbol} {self.generate_name()}')
        self.greeks = {k: v for k, v in greeks.items()}

    def get_price_data(self) -> dict[str, dict[str, float]]:
        return self.price_data

    def set_price_data(self, prices: dict[str, dict[str, float]]):
        self.price_data.update(prices)

    def set_historical_data_end(self, flag: bool = False, **kwargs):
        self.historical_data_end = flag

    def get_historical_data_end(self, **kwargs) -> bool:
        return self.historical_data_end



