from datetime import datetime
from enum import StrEnum
import json
import os
from time import sleep

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QTableWidgetItem, QGraphicsOpacityEffect

from core import Core, CoreDistributor

type CoreObj = 'CoreObj'
type QtObj = 'QtObj'


class BoxSpread:
    def __init__(self):

        self.core: Core = CoreDistributor.get_core()

        self.tab_registry = self.core.widget_registry['box_spread']

        self.register_events()

        self.selection_options: dict[str, dict[str, dict[str, str]]] = self.load_selection_options()
        self.box_spread_type = BoxSpreadType.LEND
        self.box_spread_type_btn(change=False)

        self.handle_widgets()

    def register_events(self):
        self.tab_registry['btn_type'].clicked.connect(lambda: self.box_spread_type_btn(change=True))
        self.tab_registry['comboBox_currency'].currentIndexChanged.connect(lambda: self.currency_selected())

        self.tab_registry['comboBox_index'].currentIndexChanged.connect(lambda: self.index_selected())

        self.tab_registry['slider_rate'].sliderMoved.connect(lambda x: print(123, x))
        self.tab_registry['slider_rate'].setEnabled(False)

        self.opacity_effect = QGraphicsOpacityEffect(self.tab_registry['slider_rate']).setOpacity(0.25)
        self.tab_registry['slider_rate'].setGraphicsEffect(self.opacity_effect)

        
    def currency_selected(self):
        selected_currency = self.tab_registry['comboBox_currency'].currentText()

        self.tab_registry['comboBox_index'].clear()
        self.tab_registry['comboBox_index'].addItems(self.selection_options['currencies'][selected_currency].keys())
        self.tab_registry['comboBox_expiry'].clear()

    def index_selected(self):
        selected_index = self.tab_registry['comboBox_index'].currentText()
        print(f'{selected_index} selected')

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
        self.tab_registry['comboBox_currency'].addItems(self.selection_options['currencies'].keys())

    @staticmethod
    def load_selection_options():
        selection_json_file = 'box_spread_selection_options.json'
        selection_json_path = os.path.join(os.path.dirname(__file__), selection_json_file)

        if not os.path.exists(selection_json_path):
            raise FileNotFoundError(f"Selection options file '{selection_json_file}' not found.")

        with open(selection_json_path, 'r') as file:
            selection_options = json.load(file)

        return selection_options


class BoxSpreadType(StrEnum):
    LEND = 'LEND'
    BORROW = 'BORROW'

