from time import sleep

from services.beta_weighted_deltas.beta_weighted_deltas import calculate_beta, get_portfolio_positions, build_position_instances, generate_header_lines, update_selection_list, \
    request_position_greeks, generate_table_strings, filter_positions
from services.beta_weighted_deltas.formatter import TableContentGenerator
from services.tws_api import TWSCon

type CoreObj = 'CoreObj'

class TWSRequests:
    def __init__(self, core: CoreObj):
        self.core = core
        self.tws_api = TWSCon(core)

    def check_account_id(self) -> bool:
        if self.core.account_list and self.core.account_id in self.core.account_list:
            #print(self.core.account_list)
            return True
        return False

    def control_loop(self):

        # TODO: Active tab Enum in core to define update loop by active tab
            # Move single tab logic into folders
        if not self.check_account_id():
            ...  # TODO: account_id selection popup

        startup = {'BWD': True}
        positions = []
        while True:
            if self.core.active_tab == 'beta_weighted_deltas':
                get_portfolio_positions(core=self.core, tws_api=self.tws_api)
            sleep(5)

            positions = build_position_instances(core=self.core, old_positions=positions)

            positions = filter_positions(positions=positions)  # TODO: Add support for further types
            positions_str_sorted = update_selection_list(core=self.core, positions=positions)

            calculate_beta(positions=positions, core=self.core, tws_api=self.tws_api)

            pos_headers = generate_header_lines(core=self.core, positions_str_sorted=positions_str_sorted)

            request_position_greeks(core=self.core, tws_api=self.tws_api, positions=positions)

            tcg = TableContentGenerator(core=self.core)  # Dataclass to store table content strings

            generate_table_strings(tcg=tcg, pos_headers=pos_headers, positions=positions)

            # # if activa_tab == BWD
            # if startup['BWD']:
            #     self.core.item_register['underlying_selection_list'].setCurrentRow(0)
            #     startup['BWD'] = False
            #


















            # filtered_positions = {[x.get_greeks() for x in filtered_positions]}
            # print(pos, filtered_positions)

            #         self.reqMktData(self.req_id, req_contract, '13', True, False, [])
            #
            #         while self.req_id not in self.req_greeks.keys():
            #             time.sleep(0.5)
            #
            #         self.greek_assigns[self.req_id] = [k, i]
            #         self.req_id += 1
            #
            #



