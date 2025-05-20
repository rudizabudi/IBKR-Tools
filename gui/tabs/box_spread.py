from datetime import datetime
from enum import StrEnum
import json
from threading import Thread, Event as TEvent
import os

from core import Core, CoreDistributor
from services.box_spread.request_prices import IndexPrice
from services.box_spread.request_expiries import BXSOptionChainData, BXSIndexContracts, request_index_expiries
from services.contracts import create_index_contract

type CoreObj = 'CoreObj'
type QtObj = 'QtObj'


class BoxSpread:
    def __init__(self):

        self.core: Core = CoreDistributor.get_core()

        self.tab_registry = self.core.widget_registry['box_spread']

        self.started_up = False

        self.selection_data: dict[str, dict[str, dict[str, str]]] = self.load_selection_data()
        self.box_spread_type = BoxSpreadType.LEND
        self.box_spread_type_btn(change=False)

        self.handle_widgets()
        self.register_events()

    def register_events(self):
        self.tab_registry['btn_type'].clicked.connect(lambda: self.box_spread_type_btn(change=True))

        self.tab_registry['comboBox_currency'].currentIndexChanged.connect(lambda: (print('a'), self.input_dependency_manager()))
        self.tab_registry['comboBox_index'].currentIndexChanged.connect(lambda x: (print('b', x), self.input_dependency_manager()))
        self.tab_registry['comboBox_type'].currentIndexChanged.connect(lambda: (print('c'), self.input_dependency_manager()))

        self.tab_registry['slider_rate'].sliderMoved.connect(lambda x: print(123, x))

    def first_show(self):
        if not self.started_up:
            self.toggle_comboBox(self.tab_registry['comboBox_currency'])
            self.started_up = True

    def input_dependency_manager(self):
        print('IDM started.')
        input_widgets = (self.tab_registry['comboBox_currency'], self.tab_registry['comboBox_index'], self.tab_registry['comboBox_type'])
        tmp_blocked_events = [x.blockSignals(True) for x in input_widgets]

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

        #Index
        selected_type = self.tab_registry['comboBox_type'].currentText()

        data = {'currency': selected_currency, 'index': selected_index}
        self.core.threading_events['bxs_contract_details_received'] = None
        index_request_thread = None
        if (current_contract := BXSIndexContracts.get_contract(index=selected_index)) is None:
            current_contract = create_index_contract(data=data, json_data=self.selection_data)
            BXSIndexContracts.set_contract(index=selected_index, contract=current_contract)

            self.core.threading_events['bxs_contract_details_received'] = TEvent()

            if not all([x in BXSOptionChainData.cached_symbols for x in current_contract.types.keys()]):
                index_request_thread = Thread(target=request_index_expiries, args=(current_contract,), daemon=True)
                index_request_thread.start()

        self.tab_registry['comboBox_type'].clear()
        self.tab_registry['comboBox_type'].addItems(self.selection_data['currencies'][data['currency']][data['index']]['types'].values())
        if (selection := self.tab_registry['comboBox_type'].findText(selected_type)) != -1:
            self.tab_registry['comboBox_type'].setCurrentIndex(selection)
        else:
            self.tab_registry['comboBox_type'].setCurrentIndex(0)
            selected_type = self.tab_registry['comboBox_type'].currentText()

        #Type
        types = self.selection_data['currencies'][selected_currency][selected_index]['types']

        type_ticker = [k for k, v in types.items() if v == selected_type][0]

        if self.core.threading_events['bxs_contract_details_received']:
            self.core.threading_events['bxs_contract_details_received'].wait()
            if isinstance(index_request_thread, Thread):
                index_request_thread.join()

        expiries_sorted = list(dict.fromkeys(sorted(BXSOptionChainData.expiries[type_ticker])))

        expiries = [datetime.strftime(x, '%d%b%y') for x in expiries_sorted]

        selected_expiry = self.tab_registry['comboBox_expiry'].currentText()
        self.tab_registry['comboBox_expiry'].clear()
        self.tab_registry['comboBox_expiry'].addItems(expiries)
        if (selection := self.tab_registry['comboBox_expiry'].findText(selected_expiry)) != -1:
            self.tab_registry['comboBox_expiry'].setCurrentIndex(selection)
        else:
            self.tab_registry['comboBox_expiry'].setCurrentIndex(0)
        selected_expiry = self.tab_registry['comboBox_expiry'].currentText()

        #Price
        if selected_index:
            self.core.threading_events['bxs_contract_price_received'] = TEvent()
            price_request_thread = Thread(target=IndexPrice.request_price, args=(current_contract,), daemon=True)
            price_request_thread.start()

            self.core.threading_events['bxs_contract_price_received'].wait()
            price_request_thread.join()

            price_text = f'Price: {IndexPrice.get_price(current_contract):,.0f}'
        else:
            price_text = 'Price:'

        self.tab_registry['label_price'].setText(price_text)

        print('Price set')


        for widget, block in zip(input_widgets, tmp_blocked_events):
            widget.blockSignals(block)

        print('IDM ended.')

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



class BoxSpreadType(StrEnum):
    LEND = 'LEND'
    BORROW = 'BORROW'
