from threading import Timer, Event
from time import perf_counter, perf_counter_ns
from gui.tabs.tabs import Tabs
from services.beta_weighted_deltas.beta_weighted_deltas import get_stk_beta_price, get_portfolio_positions, build_positions, generate_header_lines, build_selection_list, \
    request_position_greeks, generate_table_strings


class Backend:

    @classmethod
    def to_cls(cls, core):
        cls.core = core

    def check_account_id(self) -> bool:
        if self.core.account_list and self.core.ACCOUNT_ID in self.core.account_list:
            #print(self.core.account_list)
            return True
        return False

    @classmethod
    def beta_weighted_deltas(cls):
        t0 = perf_counter_ns()
        get_portfolio_positions()
        t1 = perf_counter_ns()
        print(f'Requesting positions took {(t1 - t0) / 1_000_000_000:.2f} sec')
        print(f'Controller 1')
        positions = build_positions()
        print(f'Controller 3')
        positions_str_sorted = build_selection_list(positions=positions)
        print(f'Controller 4')
        t2 = perf_counter_ns()
        get_stk_beta_price(positions=positions)
        t3 = perf_counter_ns()
        print(f'Requesting betas took {(t3 - t2) / 1_000_000_000:.2f} sec')
        print(f'Controller 5')
        pos_headers = generate_header_lines(positions_str_sorted=positions_str_sorted)
        print(f'Controller 6')
        t4 = perf_counter_ns()
        request_position_greeks(positions=positions)
        t5 = perf_counter_ns()
        print(f'Requesting greeks took {(t5 - t4) / 1_000_000_000:.2f} sec')
        print(f'Controller 8')
        generate_table_strings(pos_headers=pos_headers, positions=positions)
        print(f'Controller 9')

        cls.core.threading_events['bwd_list_updating'] = Event()
        cls.core.tab_instances['beta_weighted_deltas'].tab_trigger['selection_list'].fire(current_positions=positions_str_sorted)
        cls.core.threading_events['bwd_list_updating'].wait()

        cls.core.tab_instances['beta_weighted_deltas'].tab_trigger['table_greeks'].fire()

        print(f'Controller 10', cls.core.active_tab)
        if cls.core.active_tab == Tabs.BWD:
            thread = Timer(cls.core.settings['beta_weighted_deltas']['update_interval_secs'], cls.beta_weighted_deltas)
            thread.daemon = True

            thread.start()


    #     if not self.check_account_id():
    #         ...  # TODO: ACCOUNT_ID selection popup











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



