from datetime import datetime
from ibapi.contract import Contract as ibContract

type ContractObj = 'ContractObj'


class Position:
    def __init__(self, core, **kwargs):
        self.core = core

        # KWARGS
        # {'contract': {'symbol': 'VALE', 'secType': 'OPT', 'currency': 'USD', 'right': 'C', 'strike': 10.5, 'lastTradeDateOrContractMonth': '20241025', 'conId': 727068884},
        #  'position': -1.0, 'marketPrice': 0.59565555, 'marketValue': -59.57, 'averageCost': 35.2929, 'unrealizedPNL': -24.27, 'realizedPNL': 0.0}

        for key in list(kwargs.keys())[1:]:
            #print(key, kwargs[key])
            setattr(self, key, kwargs[key])

        self.contract = ibContract()
        self.contract.symbol = kwargs['contract']['symbol']
        self.contract.secType = kwargs['contract']['secType']
        self.contract.exchange = kwargs['contract'].get('exchange', 'SMART')
        self.contract.currency = kwargs['contract']['currency']
        if kwargs['contract']['secType'] in ('OPT', 'FOP'):
            self.contract.right = kwargs['contract']['right']
            self.contract.strike = float(kwargs['contract']['strike'])
            self.contract.lastTradeDateOrContractMonth = kwargs['contract']['lastTradeDateOrContractMonth']
            if kwargs['contract']['secType'] == 'FOP':
                self.contract.multiplier = "50"

        self.symbol = self.contract.symbol
        self.greeks = {}
        self.price_data = {}
        self.historical_data_end = False

    def __str__(self) -> str:
        match self.contract.secType:
            case 'STK':
                return f'<Data Container Instance> {self.contract.symbol} {self.contract.secType}'
            case 'OPT':
                dt_s: str = datetime.strptime(self.contract.lastTradeDateOrContractMonth, "%Y%m%d").strftime("%d%b%y")
                return f'<Data Container Instance> {self.contract.symbol} {self.contract.strike}{self.contract.right} {dt_s} {self.contract.secType}'

    def generate_name(self) -> str:
        match self.contract.secType:
            case 'STK':
                return f'{self.contract.symbol} Stock'
            case 'OPT' | 'FOP':
                return f'{self.contract.strike} {'Call' if self.contract.right == 'C' else 'Put'} {self.get_expiry(output_str_format='%d%b%y')}'
            case _:
                raise Exception(f'Contract type {self.contract.secType} not supported.')

    def get_contract(self) -> ContractObj:
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

    def get_greeks(self) -> dict[str: float]:
        return self.greeks

    def get_identifier(self) -> dict[str: int | str]:
        return {'name': self.generate_name(), 'pos': self.position}

    def get_pos_size(self) -> str:
        return self.position

    def get_price(self) -> float:
        return self.marketPrice

    def get_qty(self) -> float:
        return self.position

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

    def get_price_data(self) -> dict[datetime: list[float]]:
        return self.price_data

    def set_price_data(self, prices: dict[datetime: list[float]]):
        self.price_data.update(prices)

    def set_historical_data_end(self, flag: bool = False, **kwargs):
        self.historical_data_end = flag

    def get_historical_data_end(self, **kwargs) -> bool:
        return self.historical_data_end


class Header:
    def __init__(self, core, symbol: str = None, **kwargs):
        self.core = core
        self.symbol = symbol

        self.beta = None

    def add_position(self, position: Position):
        self.positions.append(position)

    def set_beta(self, beta: float):
        self.beta = beta

    def generate_name(self) -> str:
        return self.symbol

    def get_beta(self) -> float:
        return self.beta


