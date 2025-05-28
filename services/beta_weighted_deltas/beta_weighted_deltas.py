from collections import defaultdict
from datetime import datetime
from time import sleep
from ibapi.contract import Contract as ibContract

from pandas import DataFrame as df
from PySide6.QtCore import QObject, Signal
from threading import Event

from core import CoreDistributor, ReqId
from services.beta_weighted_deltas.cache import StockCache
from services.beta_weighted_deltas.formatter import generate_selection_list, TableContentGenerator
from services.beta_weighted_deltas.header import Header
from services.beta_weighted_deltas.positions import Position
from services.tws_api import  TWSConDistributor


def get_portfolio_positions():

    core = CoreDistributor.get_core()
    con = TWSConDistributor.get_con()

    core.bwd_raw_positions = {}
    core.threading_events['bwd_reqAccountUpdates'] = Event()

    con.reqAccountUpdates(True, core.ACCOUNT_ID)
    core.threading_events['bwd_reqAccountUpdates'].wait()

    con.reqAccountUpdates(False, core.ACCOUNT_ID)


def build_positions() -> list[Position]:
    core = CoreDistributor.get_core()

    positions = []

    for k in core.raw_positions.keys(): #TODO: Move raw positions to dedicated class
        if filter_raw_position(position=core.raw_positions[k]):
            pos = Position(core=core, **core.raw_positions[k])
            positions.append(pos)

    positions = list(set(positions))

    return positions


def filter_raw_position(position: dict[str, ibContract | str | int | float]) -> bool:
    filter_type = True
    SUPPORTED_TYPES = ('STK', 'OPT', 'FOP')

    filter_currency = True
    SUPPORTED_CURRENCIES = ('USD',)

    filter_qty = True
    MINIMUM_QTY = 0  # exclusive

    if filter_type:
        if position['contract']['secType'] not in SUPPORTED_TYPES:
            return False

    if filter_currency:
        if position['contract']['currency'] not in SUPPORTED_CURRENCIES:
            return False

    if filter_qty:
        if position['position'] <= MINIMUM_QTY:
            return False

    return True

class UpdateSelectionList(QObject):
    trigger_selection_list_update = Signal(list)

    def __init__(self):
        super().__init__()

    def fire(self, current_positions: list[str]):
        self.trigger_selection_list_update.emit(current_positions)


def build_selection_list(positions: list[Position]) -> list[str]:
    sl_positions = ['Overview', 'Portfolio']
    sl_positions.extend(sorted(list(set(x.get_symbol() for x in positions))))

    return sl_positions


def get_stk_beta_price(positions: list[Position]):
    unique_underlyings = set([x.get_symbol() for x in positions])

    benchmark_positon = Position(benchmark=True)

    request_historical_data(position=benchmark_positon)

    bench_hist = df({'close': [x['close'] for x in benchmark_positon.get_price_data().values()]})
    bench_hist['change'] = bench_hist['close'].pct_change()

    core = CoreDistributor.get_core()
    beta_pos_dummies = {x: Position(core=core, **{'contract': {'symbol': x, 'secType': 'STK', 'currency': 'USD', 'exchange': 'SMART'}}) for x in unique_underlyings}

    bench_var = bench_hist['change'].var()
    for symbol, pos in beta_pos_dummies.items():
        if pos not in StockCache.betas.keys():
            request_historical_data(position=beta_pos_dummies[symbol])
            stock_hist = df({'close': [x['close'] for x in beta_pos_dummies[symbol].get_price_data().values()]})
            stock_hist['change'] = stock_hist['close'].pct_change()

            StockCache.underlying_prices[pos] = float(round(stock_hist.iloc[-1]['close'], 2))

            covariance = stock_hist['change'].cov(bench_hist['change'])
            beta = float(round(covariance / bench_var, 3))

            StockCache.betas[pos] = beta


def generate_header_lines(positions_str_sorted: list[str]) -> dict[str, Header]:
    pos_headers = {}
    for symbol in positions_str_sorted:
        header = Header(symbol=symbol)
        if symbol not in ['Overview', 'Portfolio']:
            header.set_beta(StockCache.get_beta(symbol=symbol))
        pos_headers[symbol] = header

    return pos_headers


def request_position_greeks(positions: list[Position]):
    core = CoreDistributor.get_core()
    con = TWSConDistributor.get_con()

    OPTION_TYPES = ('FOP', 'OPT')

    for position in positions:
        contract = position.get_contract()
        if contract.secType in OPTION_TYPES and datetime.today().date() <= position.get_expiry(dt_object=True).date():
            core.threading_events['bwd_reqGreeks'] = Event()

            reqId = ReqId.register_reqId(position.set_greeks)
            con.reqMktData(reqId, contract, '13', True, False, []) # TODO: Test subscription

            core.threading_events['bwd_reqGreeks'].wait()


class UpdateTableGreeks(QObject):
    trigger_table_update = Signal()

    def __init__(self):
        super().__init__()

    def fire(self):
        self.trigger_table_update.emit()


def generate_table_strings(pos_headers: dict[str, Header], positions: list[Position], inject_dummies: bool = False):
    core = CoreDistributor.get_core()
    tcg = TableContentGenerator()

    if not inject_dummies:
        for underlying in pos_headers.keys():
            header = {'name': pos_headers[underlying].generate_name(),
                      'beta': pos_headers[underlying].get_beta(),
                      'symbol': underlying}

            filtered_positions = list(filter(lambda x: x.get_symbol() == underlying, positions.copy()))
            tcg.generate_position_cells(header=header, positions=filtered_positions)

        tcg.calculate_total_line()
        tcg.generate_overview_cells()
        tcg.generate_portfolio_cells()

    else:
        tcg.inject_dummy()


def request_historical_data(position: Position):
    core = CoreDistributor.get_core()
    con = TWSConDistributor.get_con()

    reqId = ReqId.register_reqId(position.set_price_data)

    core.threading_events['bwd_reqHistoricalData'] = Event()

    con.reqHistoricalData(reqId=reqId,
                          contract=position.get_contract(),
                          endDateTime=datetime.today().strftime("%Y%m%d-%H:%M:%S"),
                          durationStr='1 Y',
                          barSizeSetting='1 day',
                          whatToShow="Bid_Ask",
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])

    core.threading_events['bwd_reqHistoricalData'].wait()


def filter_supported_types(positions: list[Position]) -> list[Position]:
    positions = list(filter(lambda x: x.get_qty() > 0, positions))
    return positions
