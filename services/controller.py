from ibapi.contract import Contract as ibContract
from time import sleep

from core import CoreDistributor
from services.tws_api import TWSConDistributor
from gui.tabs.tabs import Tabs
from services.beta_weighted_deltas.beta_weighted_deltas import calculate_beta, get_portfolio_positions, build_position_instances, generate_header_lines, update_selection_list, \
    request_position_greeks, generate_table_strings, filter_positions
from services.beta_weighted_deltas.formatter import TableContentGenerator
from services.box_spread.request_expiries import BXSOptionChainData, BXSIndexContracts, request_index_expiries
from services.box_spread.request_prices import IndexPrice


class Backend:
    def __init__(self):
        self.core = CoreDistributor.get_core()
        self.tws_con = TWSConDistributor.get_con()

        self.bxs_previous_contract = ''

    def check_account_id(self) -> bool:
        if self.core.account_list and self.core.ACCOUNT_ID in self.core.account_list:
            #print(self.core.account_list)
            return True
        return False

    def control_loop(self):

        # TODO: Active tab Enum in core to define update loop by active tab
            # Move single tab logic into folders
        if not self.check_account_id():
            ...  # TODO: ACCOUNT_ID selection popup

        bxs_previous_contract: ibContract = None

        positions = []
        bxs_started = False
        while True:
            match self.core.active_tab:
                case Tabs.BWD:
                    get_portfolio_positions(core=self.core, con=self.tws_con)

                    positions = build_position_instances(core=self.core, old_positions=positions)

                    positions = filter_positions(positions=positions)  # TODO: Add support for further types

                    positions_str_sorted = update_selection_list(core=self.core, positions=positions)

                    calculate_beta(core=self.core, positions=positions, con=self.tws_con)

                    pos_headers = generate_header_lines(core=self.core, positions_str_sorted=positions_str_sorted)

                    request_position_greeks(core=self.core, con=self.tws_con, positions=positions)

                    tcg = TableContentGenerator()  # Dataclass to store table content strings

                    generate_table_strings(tcg=tcg, pos_headers=pos_headers, positions=positions)

                    self.core.tab_instances['beta_weighted_deltas'].change_table_content()

                    sleep(self.core.controller_loop_interval)

                case Tabs.BXS:
                    # try:
                    #     #current_contract = self.core.bxs_index_contract[self.core.widget_registry['box_spread']['comboBox_index'].currentText()]
                    #     current_contract = BXSIndexContracts.get_active_contract()
                    #     if current_contract:
                    #         if not all([x in BXSOptionChainData.cached_symbols for x in current_contract.types.keys()]):
                    #             request_index_expiries(index_contract=current_contract, con=self.tws_con)
                    #
                    #             IndexPrice.request_price(index_contract=current_contract)
                    #
                    # except KeyError as e:
                    #     print(345, e)
                    #     pass
                    pass
            sleep(0.1)



















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



