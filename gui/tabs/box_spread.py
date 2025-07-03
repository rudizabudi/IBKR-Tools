from datetime import datetime, timedelta
from enum import StrEnum
from ibapi.contract import Contract as ibContract
import json
from threading import Event as TEvent, Lock, Thread
import os

from core import Core, CoreDistributor
from services.box_spread.request_prices import ContractPrices
from services.box_spread.requests_misc import BXSOptionChainData, BXSIndexContracts, request_index_expiries
from services.box_spread.request_bxs_options import request_bxs_option_prices
from services.box_spread.check_existence import check_strikes, ContractExistence, UpdateGuiStrikes
from services.contracts import build_index_contract


class BoxSpread:
    def __init__(self):
        super().__init__()
        self.core: Core = CoreDistributor.get_core()

        self.tab_registry = self.core.widget_registry['box_spread']

        self.started_up = False

        self.selection_data: dict[str, dict[str, dict[str, str]]] = self.load_selection_data()
        self.box_spread_type = BoxSpreadType.LEND
        self.box_spread_type_btn(change=False)

        self.tab_trigger = {'strikes': UpdateGuiStrikes()}

        self.handle_widgets()
        self.register_events()

    def register_events(self):
        self.tab_registry['btn_type'].clicked.connect(lambda: self.box_spread_type_btn(change=True))

        self.tab_registry['comboBox_currency'].currentIndexChanged.connect(lambda: (print('a'), self.input_dependency_manager()))
        self.tab_registry['comboBox_index'].currentIndexChanged.connect(lambda x: (print('b', x), self.input_dependency_manager()))
        self.tab_registry['comboBox_type'].currentIndexChanged.connect(lambda: (print('c'), self.input_dependency_manager()))
        self.tab_registry['comboBox_upper_strike'].currentIndexChanged.connect(lambda: (print('d'), self.input_dependency_manager()))
        self.tab_registry['comboBox_lower_strike'].currentIndexChanged.connect(lambda: (print('e'), self.input_dependency_manager()))
        self.tab_registry['comboBox_expiry'].currentIndexChanged.connect(lambda: (print('f'), self.input_dependency_manager()))

        self.tab_registry['line_amount'].textEdited.connect(lambda: (print('g'), self.input_dependency_manager()))

        self.tab_trigger['strikes'].trigger_strike_update.connect(self.set_strike_comboBoxes)
        self.tab_registry['slider_rate'].sliderMoved.connect(lambda x: print(123, x))

    def tester(self):
        print('Signal received')

    def init_activity(self):
        if not self.started_up:
            self.toggle_comboBox(self.tab_registry['comboBox_currency'])
            self.started_up = True

    def input_dependency_manager(self):
        input_widgets = (self.tab_registry['comboBox_currency'], self.tab_registry['comboBox_index'], self.tab_registry['comboBox_type'],
                         self.tab_registry['comboBox_upper_strike'], self.tab_registry['comboBox_lower_strike'],
                         self.tab_registry['comboBox_expiry'])

        tmp_blocked_events = [x.blockSignals(True) for x in input_widgets]

        #direction
        selected_direction = self.box_spread_type

        #Currency
        selected_currency = self.tab_registry['comboBox_currency'].currentText()
        selected_index = self.tab_registry['comboBox_index'].currentText()

        self.tab_registry['comboBox_index'].clear()
        self.tab_registry['comboBox_index'].addItems(self.selection_data['currencies'][selected_currency].keys())
        if (selection := self.tab_registry['comboBox_index'].findText(selected_index)) != -1:
            self.tab_registry['comboBox_index'].setCurrentIndex(selection)
        else:
            self.tab_registry['comboBox_index'].setCurrentIndex(0)
            selected_index = self.tab_registry['comboBox_index'].currentText()

        data = {'currency': selected_currency, 'index': selected_index}
        self.core.threading_events['bxs_contract_details_received'] = None
        index_request_thread = None
        if (current_contract := BXSIndexContracts.get_contract(index=selected_index)) is None:
            current_contract = build_index_contract(data=data, json_data=self.selection_data)
            BXSIndexContracts.set_contract(index=selected_index, contract=current_contract)

            # self.core.threading_events['bxs_contract_details_received'] = TEvent()

            if not all([x in BXSOptionChainData.cached_symbols for x in current_contract.types.keys()]):
                index_request_thread = Thread(target=request_index_expiries, args=(current_contract,), daemon=True)
                print('t1')
                self.core.threading_events['bxs_contract_details_received'] = TEvent()
                index_request_thread.start()
                print('t2')

        # Type
        selected_type = self.tab_registry['comboBox_type'].currentText()
        self.tab_registry['comboBox_type'].clear()
        self.tab_registry['comboBox_type'].addItems(self.selection_data['currencies'][data['currency']][data['index']]['types'].values())
        if (selection := self.tab_registry['comboBox_type'].findText(selected_type)) != -1:
            self.tab_registry['comboBox_type'].setCurrentIndex(selection)
        else:
            self.tab_registry['comboBox_type'].setCurrentIndex(0)
            selected_type = self.tab_registry['comboBox_type'].currentText()

        types = self.selection_data['currencies'][selected_currency][selected_index]['types']

        #type_ticker = [k for k, v in types.items() if v == selected_type][0]
        selected_type_ticker = [k for k, v in self.selection_data['currencies'][selected_currency][selected_index]['types'].items() if v == selected_type][0]
        current_contract.selected_type = selected_type_ticker
        print(f'{selected_type_ticker}')

        if self.core.threading_events['bxs_contract_details_received']:
            self.core.threading_events['bxs_contract_details_received'].wait()
            if isinstance(index_request_thread, Thread):
                print('t3')
                index_request_thread.join()
                print('t4')
        print(1)

        # Expiries
        expiries_sorted = list(dict.fromkeys(sorted(BXSOptionChainData.expiries[selected_type_ticker])))

        expiries = [datetime.strftime(x, '%d%b%y') for x in expiries_sorted if x >= (datetime.now() + timedelta(days=self.core.settings['box_spread']['minimum_expiration_days']))]

        selected_expiry = self.tab_registry['comboBox_expiry'].currentText()
        self.tab_registry['comboBox_expiry'].clear()
        self.tab_registry['comboBox_expiry'].addItems(expiries)
        if (selection := self.tab_registry['comboBox_expiry'].findText(selected_expiry)) != -1:
            self.tab_registry['comboBox_expiry'].setCurrentIndex(selection)
        else:
            self.tab_registry['comboBox_expiry'].setCurrentIndex(0)
            selected_expiry = self.tab_registry['comboBox_expiry'].currentText()
        print(2)

        #multiplier
        if multiplier := BXSOptionChainData.multipliers[selected_type_ticker][0]:
            multiplier_text = f'Multiplier: {int(multiplier)}'
        else:
            multiplier_text = f'Multiplier: -'

        self.tab_registry['label_multiplier'].setText(multiplier_text)


        #Price
        if selected_index:
            self.core.threading_events['bxs_reqHistoricalData'] = TEvent()
            price_request_thread = Thread(target=ContractPrices.request_price_tws, args=(current_contract,), daemon=True)
            price_request_thread.start()

            self.core.threading_events['bxs_reqHistoricalData'].wait()
            price_request_thread.join()

            price_text = f'Price: {ContractPrices.get_price(current_contract):,.0f}'
        else:
            price_text = 'Price:'

        self.tab_registry['label_underlying_price'].setText(price_text)

        if not selected_expiry:
            return

        #strikes
        selected_expiry_dt = datetime.strptime(selected_expiry, '%d%b%y')
        # checking_strikes_thread = Thread(target=check_strikes, args=(current_contract, selected_expiry_dt, self), daemon=True)
        # checking_strikes_thread.start()

        check_strikes(current_contract, selected_expiry_dt, self)
        print('t8')

        selected_lower_strike = float(self.tab_registry['comboBox_lower_strike'].currentText())
        selected_upper_strike = float(self.tab_registry['comboBox_upper_strike'].currentText())

        # if isinstance(self.core.threading_events['check_contract_existence'], TEvent) and not self.core.threading_events['check_contract_existence'].is_set():
        #     print('t8.5')
        #     return

        print('t9')
        request_bxs_option_prices(index_contract=current_contract,
                                  expiry_date=selected_expiry_dt,
                                  lower_strike=selected_lower_strike,
                                  upper_strike=selected_upper_strike,
                                  direction=selected_direction)
        print('t10')

        spread = self.set_spread_text()

        # Redemption
        amount = None
        try:
            amount = int(self.tab_registry['line_amount'].text())
        except ValueError:
            pass

        if all([amount, multiplier, spread]):
            redemption = spread * multiplier * amount
            print([amount, multiplier, spread, redemption])

            self.tab_registry['label_redemption'].setText(f'Redemption: {redemption:,.0f}')
        else:
            self.tab_registry['label_redemption'].setText(f'Redemption:')

        for widget, block in zip(input_widgets, tmp_blocked_events):
            widget.blockSignals(block)

        print('IDM ended.')

    def set_strike_comboBoxes(self, current_contract: ibContract, strikes: list[float] = None):

        input_widgets = (self.tab_registry['comboBox_upper_strike'], self.tab_registry['comboBox_lower_strike'])
        tmp_blocked_events = [x.blockSignals(True) for x in input_widgets]

        _lock = Lock()
        print('Set strike comboboxes', current_contract)
        if strikes is None:
            selected_expiry = self.tab_registry['comboBox_expiry'].currentText()
            selected_expiry_dt = datetime.strptime(selected_expiry, '%d%b%y')
            strikes = ContractExistence.get_valid_strikes(current_contract, selected_expiry_dt)
            print(f'Len new strikes: {len(strikes)}')

        with _lock:
            upper_strikes = list(filter(lambda x: x >= ContractPrices.get_price(current_contract), strikes))
            upper_strikes = sorted([str(x) for x in upper_strikes], key=lambda x: float(x), reverse=True)
            lower_strikes = list(filter(lambda x: x <= ContractPrices.get_price(current_contract), strikes))
            lower_strikes = sorted([str(x) for x in lower_strikes], key=lambda x: float(x), reverse=True)

            selected_upper_strike = self.tab_registry['comboBox_upper_strike'].currentText()
            self.tab_registry['comboBox_upper_strike'].clear()
            self.tab_registry['comboBox_upper_strike'].addItems(upper_strikes)
            if (selection := self.tab_registry['comboBox_upper_strike'].findText(selected_upper_strike)) != -1:
                self.tab_registry['comboBox_upper_strike'].setCurrentIndex(selection)
            else:
                count = self.tab_registry['comboBox_upper_strike'].count()
                self.tab_registry['comboBox_upper_strike'].setCurrentIndex(count - 1)
                selected_upper_strike = self.tab_registry['comboBox_upper_strike'].currentText()

            selected_lower_strike = self.tab_registry['comboBox_lower_strike'].currentText()
            self.tab_registry['comboBox_lower_strike'].clear()
            self.tab_registry['comboBox_lower_strike'].addItems(lower_strikes)
            if (selection := self.tab_registry['comboBox_lower_strike'].findText(selected_lower_strike)) != -1:
                self.tab_registry['comboBox_lower_strike'].setCurrentIndex(selection)
            else:
                self.tab_registry['comboBox_lower_strike'].setCurrentIndex(0)
                selected_lower_strike = self.tab_registry['comboBox_lower_strike'].currentText()

        for widget, block in zip(input_widgets, tmp_blocked_events):
            widget.blockSignals(block)


    def set_spread_text(self) -> float:
        try:
            selected_lower_strike = float(self.tab_registry['comboBox_lower_strike'].currentText())
            selected_upper_strike = float(self.tab_registry['comboBox_upper_strike'].currentText())
            spread = selected_upper_strike - selected_lower_strike
            spread_text = f'Spread: {selected_upper_strike - selected_lower_strike:,.0f}'
        except ValueError:
            spread = 0
            spread_text = f'Spread: --- '

        self.tab_registry['label_spread'].setText(spread_text)

        return spread

    def strike_change(self):
        self.set_spread_text()

    def handle_widgets(self):
        self.set_currency_options()

    def box_spread_type_btn(self, change: bool = False):
        if change:
            if self.box_spread_type == BoxSpreadType.LEND:
                self.box_spread_type = BoxSpreadType.BORROW
            else:
                self.box_spread_type = BoxSpreadType.LEND

        self.tab_registry['btn_type'].setText(self.box_spread_type.value)
        btn_color = 'green' if self.box_spread_type == BoxSpreadType.LEND else 'red'
        self.tab_registry['btn_type'].setStyleSheet(f'background-color: {btn_color};')

    def set_currency_options(self):
        self.tab_registry['comboBox_currency'].clear()
        self.tab_registry['comboBox_currency'].addItems(self.selection_data['currencies'].keys())

    @staticmethod
    def load_selection_data():
        selection_json_file = 'box_spread_selection_options.json'
        selection_json_path = os.path.join(os.path.dirname(__file__), selection_json_file)

        if not os.path.exists(selection_json_path):
            raise FileNotFoundError(f"Selection options file '{selection_json_file}' not found.")

        with open(selection_json_path, 'r') as file:
            selection_options = json.load(file)

        return selection_options

    @staticmethod
    def toggle_comboBox(widget) -> None:
        print('toggling')
        selection = widget.findText(widget.currentText())

        blocked_event = widget.blockSignals(True)
        widget.setCurrentIndex(-1)
        widget.blockSignals(blocked_event)
        widget.setCurrentIndex(selection)
        print('toggling_ended')

    @staticmethod
    def set_transparency(widget, transparency: int) -> None:
        match transparency:
            case 0:
                widget.setVisible(False)
            case 1:
                widget.setVisible(True)
            case _:
                raise Exception(f"Transparency value {transparency} not supported. Must be 0, 1 or 100.")

        # opacity_effect = QGraphicsOpacityEffect(widget)
        # opacity_effect.setOpacity(transparency)
        # widget.setGraphicsEffect(opacity_effect)

    def bxs_resize_event(self, new_size: int = None):
        #TODO
        ...


class BoxSpreadType(StrEnum):
    LEND = 'LEND'
    BORROW = 'BORROW'
