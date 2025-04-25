from datetime import datetime
from time import sleep

from pandas import DataFrame as df

from core import Core
from services.beta_weighted_deltas.formatter import generate_selection_list, TableContentGenerator
from services.beta_weighted_deltas.header import Header
from services.beta_weighted_deltas.positions import Position
from services.tws_api import TWSCon


def build_position_instances(core: Core, old_positions: list[Position]) -> list[Position]:
    positions = []
    old_identifiers = [x.get_identifier() for x in old_positions]
    for k in core.raw_positions.keys():
        pos = Position(core=core, **core.raw_positions[k])
        if pos.get_secType() in ['STK', 'OPT']:  # TODO: Properly handle unsupported secTypes
            if pos.get_identifier() in old_identifiers:
                positions.append(list(filter(lambda x: x.get_identifier() == pos.get_identifier(), old_positions))[0])
                #print('Keep old position.')
            else:
                positions.append(pos)
                #print('Add new position.')

    return positions


def calculate_beta(core: Core, positions: list[Position], tws_api: TWSCon):
    unique_underlyings = set([x.get_symbol() for x in positions])

    beta_pos_dummies = {x: Position(core=core, **{'contract': {'symbol': x, 'secType': 'STK', 'currency': 'USD', 'exchange': 'SMART'}}) for x in unique_underlyings}

    benchmark_positon = Position(benchmark=True)
    request_historical_data(core=core, tws_api=tws_api, position=benchmark_positon)
    bench_hist = df({'Close': [x['Close'] for x in benchmark_positon.get_price_data().values()]})
    bench_hist['Change'] = bench_hist['Close'].pct_change()

    bench_var = bench_hist['Change'].var()
    for pos in beta_pos_dummies.keys():
        if pos not in core.pos_betas.keys():
            request_historical_data(core=core, tws_api=tws_api, position=beta_pos_dummies[pos])
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


def get_portfolio_positions(core: Core, tws_api: TWSCon):
    core.raw_positions = {}
    tws_api.reqAccountUpdates(True, core.account_id)

    while not core.raw_positions:
        sleep(.1)


def request_position_greeks(core: Core, tws_api: TWSCon, positions: list[Position]):
    for pos in positions:
        contract = pos.get_contract()
        if contract.secType in ('FOP', 'OPT') and datetime.today().date() <= pos.get_expiry(dt_object=True).date():
            core.reqId_hashmap[core.reqId] = pos.set_greeks
            tws_api.reqMktData(core.reqId, contract, '13', True, False, [])
            # TODO: Test subscription
            core.reqId += 1
            sleep(.1)

    sleep(2)


def request_historical_data(core: Core, tws_api: TWSCon, position: Position):
    core.reqId_hashmap[core.reqId] = position.set_price_data

    tws_api.reqHistoricalData(reqId=core.reqId,
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

    core.reqId += 1


def update_selection_list(core: Core, positions: list[Position]) -> list[str]:
    positions_str_sorted = generate_selection_list(positions)
    core.tab_instances['beta_weighted_deltas'].refresh_selection_list(positions_str_sorted)
    return positions_str_sorted


def filter_positions(positions: list[Position]) -> list[Position]:
    filter_types = True
    filter_qty = True

    def filter_secType_currency():
        return list(filter(lambda x: x.get_secType() in ['STK', 'OPT']
                                     and x.get_currency() == 'USD', positions))

    if filter_types:
        positions = filter_secType_currency()

    def filter_by_qty():
        return list(filter(lambda x: x.get_qty() != 0, positions))

    if filter_qty:
        positions = filter_by_qty()

    return positions


def filter_supported_types(positions: list[Position]) -> list[Position]:
    positions = list(filter(lambda x: x.get_qty() > 0, positions))
    return positions
