from datetime import datetime
from time import sleep
from pandas import DataFrame as df
from PySide6.QtCore import QObject, Signal
from threading import Event


from core import Core, CoreDistributor, ReqId
from services.beta_weighted_deltas.formatter import generate_selection_list, TableContentGenerator
from services.beta_weighted_deltas.header import Header
from services.beta_weighted_deltas.positions import Position
from services.tws_api import TWSCon, TWSConDistributor


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

    for k in core.raw_positions.keys():
        if filter_position(position=core.raw_positions[k]):
            pos = Position(core=core, **core.raw_positions[k])
            positions.append(pos)

    positions = list(set(positions))
    return positions


def filter_position(position: Position) -> bool:
    filter_type = True
    SUPPORTED_TYPES = ('STK', 'OPT')

    filter_currency = True
    SUPPORTED_CURRENCIES = ('USD',)

    filter_qty = True
    MINIMUM_QTY = 0  # exclusive

    if filter_type:
        if position.get_secType() not in SUPPORTED_TYPES:
            return False

    if filter_currency:
        if position.get_currency() not in SUPPORTED_CURRENCIES:
            return False

    if filter_qty:
        if position.get_qty() <= MINIMUM_QTY:
            return False

    return True


class UpdateSelectionList(QObject):
    trigger_selection_list_update = Signal(list)

    def __init__(self):
        super().__init__()

    def start(self, current_positions: list[str]):
        self.trigger_selection_list_update.emit(current_positions)


def build_selection_list(positions: list[Position]) -> list[str]:
    core = CoreDistributor.get_core()
    sl_positions = ['Overview', 'Portfolio']
    sl_positions.extend(sorted(list(set(x.get_symbol() for x in positions))))

    core.tab_instances['beta_weighted_deltas'].tab_trigger['selection_list'].start(current_positions=sl_positions)

    return sl_positions


def calculate_beta(positions: list[Position], con: TWSCon):

    core = CoreDistributor.get_core()

    unique_underlyings = set([x.get_symbol() for x in positions])

    benchmark_positon = Position(benchmark=True)
    request_historical_data(position=benchmark_positon)
    bench_hist = df({'Close': [x['Close'] for x in benchmark_positon.get_price_data().values()]})
    bench_hist['Change'] = bench_hist['Close'].pct_change()

    beta_pos_dummies = {x: Position(core=core, **{'contract': {'symbol': x, 'secType': 'STK', 'currency': 'USD', 'exchange': 'SMART'}}) for x in unique_underlyings}

    bench_var = bench_hist['Change'].var()
    for pos in beta_pos_dummies.keys():
        if pos not in core.pos_betas.keys():
            request_historical_data(position=beta_pos_dummies[pos])
            stock_hist = df({'Close': [x['Close'] for x in beta_pos_dummies[pos].get_price_data().values()]})
            stock_hist['Change'] = stock_hist['Close'].pct_change()
            core.underlying_prices[pos] = float(round(stock_hist.iloc[-1]['Close'], 2))

            covariance = stock_hist['Change'].cov(bench_hist['Change'])
            beta = float(round(covariance / bench_var, 3))

            core.pos_betas[pos] = beta


def generate_header_lines(core: Core, positions_str_sorted: list[str]) -> dict[str: Header]:
    pos_headers = {}
    for symbol in positions_str_sorted:
        header = Header(core=core, symbol=symbol)
        if symbol not in ['Overview', 'Portfolio']:
            header.set_beta(core.pos_betas[symbol])
        pos_headers[symbol] = header

    return pos_headers


def generate_table_strings(tcg: TableContentGenerator, pos_headers: dict[str, Header], positions: list[Position], inject_dummies: bool = False):
    if not inject_dummies:
        for underlying in pos_headers.keys():
            header = {'name': pos_headers[underlying].generate_name(),
                      'beta': pos_headers[underlying].get_beta()}

            filtered_positions = list(filter(lambda x: x.get_symbol() == underlying, positions.copy()))
            tcg.generate_position_cells(header=header, positions=filtered_positions)

        tcg.calculate_total_line()
        tcg.generate_overview_cells()
        tcg.generate_portfolio_cells()
    else:
        tcg.inject_dummy()


def request_position_greeks(core: Core, con: TWSCon, positions: list[Position]):
    for position in positions:
        contract = position.get_contract()
        if contract.secType in ('FOP', 'OPT') and datetime.today().date() <= position.get_expiry(dt_object=True).date():
            reqId = ReqId.register_reqId(position.set_greeks)
            con.reqMktData(reqId, contract, '13', True, False, [])
            # TODO: Test subscription
            sleep(.1)

    sleep(2)


def request_historical_data(position: Position):
    core = CoreDistributor.get_core()
    con = TWSConDistributor.get_con()
    reqId = ReqId.register_reqId(position.set_price_data)

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

    while not position.get_historical_data_end():
        pass


def filter_supported_types(positions: list[Position]) -> list[Position]:
    positions = list(filter(lambda x: x.get_qty() > 0, positions))
    return positions
