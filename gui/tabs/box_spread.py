from datetime import datetime
from enum import StrEnum
import json
import os
from time import sleep

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QTableWidgetItem

from core import Core, CoreDistributor

type CoreObj = 'CoreObj'
type QtObj = 'QtObj'


class BoxSpread:
    def __init__(self):

        self.core: Core = CoreDistributor.get_core()

        self.tab_registry = self.core.widget_registry['beta_weighted_deltas']

        self.register_button_clicks()

        self.selection_options: dict[str, dict[str, str]] = self.load_selection_options()
        self.box_spread_type = BoxSpreadType.LEND
        self.box_spread_type_btn(change=False)

        self.handle_widgets()

    def handle_widgets(self):
        self.set_currency_options()

    def register_button_clicks(self):
        self.core.widget_registry['box_spread']['btn_type'].clicked.connect(lambda: self.box_spread_type_btn(change=True))

    def box_spread_type_btn(self, change: bool = False):
        if change:
            if self.box_spread_type == BoxSpreadType.LEND:
                self.box_spread_type = BoxSpreadType.BORROW
            else:
                self.box_spread_type = BoxSpreadType.LEND

        self.core.widget_registry['box_spread']['btn_type'].setText(self.box_spread_type.value)
        btn_color = 'green' if self.box_spread_type == BoxSpreadType.LEND else 'red'
        self.core.widget_registry['box_spread']['btn_type'].setStyleSheet(f'background-color: {btn_color};')

    def set_currency_options(self):
        self.core.widget_registry['box_spread']['comboBox_currency'].clear()
        self.core.widget_registry['box_spread']['comboBox_currency'].addItems(self.selection_options['currencies'].keys())

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

