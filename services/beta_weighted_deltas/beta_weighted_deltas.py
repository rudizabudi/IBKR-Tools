from services.beta_weighted_deltas.formatter import generate_selection_list
from services.contracts import Position, Header
from services.yf_api import calculate_beta

from datetime import datetime
from time import sleep

type CoreObj = 'CoreObj'
type HeaderObj = 'HeaderObj'
type TWSConObj = 'TWSConObj'
type TCGObj = 'TCGObj'

def build_position_instances(core: CoreObj) -> list[Position]:
    positions = []
    for k in core.raw_positions.keys():
        pos = Position(core=core, **core.raw_positions[k])
        positions.append(pos)

    return positions


def generate_header_lines(core: CoreObj, positions_str_sorted: list[str]) -> dict[str: HeaderObj]:
    pos_headers = {}
    for symbol in positions_str_sorted:
        header = Header(core=core, symbol=symbol)
        if symbol not in ['Overview', 'Portfolio']:
            header.set_beta(calculate_beta(symbol=symbol, core=core))
        pos_headers[symbol] = header

    return pos_headers


def generate_table_strings(tcg:TCGObj, pos_headers: dict[str: HeaderObj], positions:  list[Position], inject_dummies: bool = False):

    if not inject_dummies:
        for underlying in pos_headers.keys():
            header = {}
            header['name'] = pos_headers[underlying].generate_name()
            header['beta'] = pos_headers[underlying].get_beta()
            filtered_positions = list(filter(lambda x: x.get_symbol() == underlying, positions.copy()))

            tcg.generate_position_cells(header=header, positions=filtered_positions)

        tcg.calculate_total_line()
        tcg.generate_overview_cells()
        tcg.generate_portfolio_cells()
    else:
        tcg.inject_dummy()


def get_portfolio_positions(core: CoreObj, tws_api: TWSConObj):
    core.raw_positions = {}
    tws_api.reqAccountUpdates(True, core.account_id)

    while not core.raw_positions:
        sleep(.1)


def request_position_greeks(core: CoreObj, tws_api: TWSConObj, positions: list[Position]):
    for pos in positions:
        contract = pos.get_contract()
        if contract.secType in ('FOP', 'OPT') and datetime.today().date() <= pos.get_expiry(dt_object=True).date():
            core.reqId_hashmap[core.reqId] = pos.set_greeks
            tws_api.reqMktData(core.reqId, contract, '13', True, False, [])
            # TODO: Test subscription
            core.reqId += 1
            sleep(.1)

    sleep(2)


def update_selection_list(core: CoreObj, positions: list[Position]) -> list[str]:
    positions_str_sorted = generate_selection_list(positions)
    core.frame_tabs['Beta Weighted Deltas'].update_selection_list(positions_str_sorted)
    return positions_str_sorted
