from datetime import datetime
from time import sleep

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QSizePolicy, QAbstractItemView

from core import Core, CoreDistributor
from services.beta_weighted_deltas.beta_weighted_deltas import UpdateSelectionList

type CoreObj = 'CoreObj'
type QtObj = 'QtObj'


class BetaWeightedDeltas:
    def __init__(self):

        self.core: Core = CoreDistributor.get_core()
        self.table_contents = self.core.table_contents

        self.previous_selection: None | str = None

        self.symbol_list: list = ['Loading...']

        self.tab_trigger = {'selection_list': UpdateSelectionList()}

        self.tab_registry = self.core.widget_registry['beta_weighted_deltas']

        self.handle_widgets()

        self.register_events()

    def register_events(self):
        self.tab_registry['list_selection'].currentItemChanged.connect(lambda: self.change_table_content())

    def bwd_resize_event(self, new_size: int = None):
        bwd_frame = self.tab_registry['frame']
        bwd_frame.setGeometry(bwd_frame.geometry().x(), bwd_frame.geometry().y(), new_size.width() - self.core.widget_registry['misc']['leftMenuBg'].width(), new_size.height() - self.core.widget_registry['misc']['contentTopBg'].height())

        headers = ['Symbol', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', ' γ Gamma (L|S)', 'Notional position']

        bwd_table_widget = self.tab_registry['table_greeks']
        bwd_table_widget.setHorizontalHeaderLabels(headers)

        bwd_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        bwd_table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bwd_table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        bwd_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        column_ratios = {0: 3,
                         1: 7,
                         2: 3,
                         3: 3,
                         4: 4,
                         5: 7,
                         6: 4,
                         7: 6,
                         8: 5}

        for k, v in column_ratios.items():
            width = int(round((bwd_table_widget.width() / sum(column_ratios.values())) * v * .96, 0))
            bwd_table_widget.setColumnWidth(k, width)

        bwd_table_widget.horizontalHeader().setFont(QFont(self.core.project_font, 9))

        for _ in range(998):
            row_position = bwd_table_widget.rowCount()
            bwd_table_widget.insertRow(row_position)

            for column in range(bwd_table_widget.columnCount()):
                bwd_table_widget.setItem(row_position, column, QTableWidgetItem(''))

    def handle_widgets(self):
        def change_selection_list():
            selection_list = self.tab_registry['list_selection']
            selection_list.setFont(QFont("", 18))
            selection_list.addItems(self.symbol_list)
            selection_list.setMaximumWidth(200)
            selection_list.setMinimumWidth(100)
            selection_list.setMinimumHeight(500)
            selection_list.resize(200, 1245)

        #change_selection_list()

    def change_table_content(self):
        # TODO: Add sorting via 1 or 2 selection fields: sort by and ASC/DESC(?)
        # Alternative: Sort via column header click

        selection_list = self.tab_registry['list_selection']
        bwd_table = self.tab_registry['table_greeks']
        if selection_list.currentItem():
            bwd_table.clear()

            selection = selection_list.currentItem().text()
            #print(f'Selection from bwd_table check: {selection}')

            while selection not in self.core.table_contents.keys():
                sleep(.01)

            for i, x in enumerate(self.table_contents[selection]):
                for j, y in enumerate(self.table_contents[selection][i]):  # columns
                    if not y:
                        y = ''

                    item = QTableWidgetItem(str(y))
                    if i in [0] and selection not in ['Overview', 'Portfolio']:
                        item.setFont(QFont('', 8, QFont.Bold))
                    if j in [8]:
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    elif j in [1, 2, 3, 4, 5, 6, 7]:
                        item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

                    bwd_table.setItem(i, j, item)

            headers = ['Symbol', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', 'γ Gamma (L|S)', 'Notional position']
            bwd_table.setHorizontalHeaderLabels(headers)
            bwd_table.horizontalHeader().setFont(QFont(self.core.project_font, 9))
            self.previous_selection = selection

    def refresh_selection_list(self, symbol_list: list):
        selection_list = self.tab_registry['list_selection']
        selection_list.blockSignals(True)

        if selection_list.currentItem():
            selection = selection_list.currentItem().text()
        else:
            selection = None

        selection_list.clear()
        selection_list.addItems(symbol_list)

        for i in range(selection_list.count()):
            selection_list.item(i).setFont(QFont(self.core.project_font, 16))

        # Manage re-selection or default selection
        if selection in symbol_list:
            while not selection_list.currentItem() or selection_list.currentItem().text() != selection:
                try:
                    index = symbol_list.index(selection)
                    selection_list.setCurrentRow(index)  # Set intended selection
                    sleep(.1)
                except AttributeError:
                    continue
        else:
            selection_list.setCurrentRow(0)  # Default selection

        selection_list.blockSignals(False)  # Re-enable signals

    # def selection_list_change(self):
    #     try:
    #         self.change_table_content()
    #     except AttributeError:
    #         pass
    #
    # def set_symbol_list(self, symbol_list: list):
    #     self.symbol_list = symbol_list





# def change_table(self, df):
#     bwd_table.clear()
#
#     print('Change Table Current selection:', list_selection)
#     if list_selection == 'Overview':
#         df_ls = {}
#         print('Overview triggered')
#         for i, x in enumerate(df['Underlying']):
#             if not (df['Underlying'][i] == '' and df['Beta / Position'][i] != ''):
#                 for y in ['Underlying', 'Beta / Position', 'Amount', 'iVol', 'Delta', 'Beta weighted Delta', 'Theta', 'Gamma', 'Notional Position']:
#                     if y not in df_ls.keys():
#                         df_ls[y] = [df[y][i]]
#                     else:
#                         df_ls[y].append(df[y][i])
#
#         df = df_ls
#
#     for i, x in enumerate(df.keys()):  # columns
#         for j, y in enumerate(df[x]):  # rows
#             if i not in [0, 1, 2] and isinstance(y, (int, float)):
#                 y = f'{y:.2f}'
#             item = QTableWidgetItem(str(y))
#             if i in [8]:
#                 item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             elif i in [1, 2, 3, 4, 5, 6, 7, ]:
#                 item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
#
#             # if list_selection !='Overview' or (list_selection =='Overview' and (df[list(df.keys())[0]][i] == df[list(df.keys())[1]][i] or df[list(df.keys())[1]][i] != '')):
#             bwd_table.setItem(j, i, item)
#             # item.setForeground(QtGui.QBrush(QtGui.QColor(0, 128, 0)))
#
#     headers = ['Underlying', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', 'γ Gamma (L|S)', 'Notional position']
#     bwd_table.setHorizontalHeaderLabels(headers)
#     bwd_table.viewport().update()
#
#     last_update = dt.now().strftime('%H:%M')
#     refresh_label.setText(f"{'Last update: ':>20}{last_update}")
#
#
# def change_list(self, positions):
#     list_widget.clear()
#     list_items = ['Portfolio', 'Overview']
#     for x in positions.keys():
#         list_items.append(str(x))
#     list_widget.addItems(list_items)
#
#     # print(list_selection)
#     list_order = {}
#     for x in range(list_widget.count()):
#         list_order[list_widget.item(x).text()] = x
#
#     if list_selection is not None:
#         list_widget.setCurrentRow(list_order[list_selection])
#     elif old_selection is not None:
#         list_widget.setCurrentRow(list_order[old_selection])
#     else:
#         list_widget.setCurrentRow(0)
#
#     list_widget.viewport().update()
#
#
# def handle_list_selection(self, current_item):
#     global list_selection
#     # print('Start Handle List Current selection:', list_selection)
#     # print('Start Handle List Old selection:', old_selection)
#
#     if current_item is None:
#         list_selection = old_selection
#     else:
#         list_selection = current_item.text()
#
#     # print('End Handle List Current selection:', list_selection)
#     # print('End Handle List Old selection:', old_selection)
#
#
# def resizeEvent(self, event: QResizeEvent):
#     column_ratios = {0: 4,
#                      1: 7,
#                      2: 2,
#                      3: 3,
#                      4: 4,
#                      5: 7,
#                      6: 4,
#                      7: 5,
#                      8: 6}
#
#     for k, v in column_ratios.items():
#         width = int(round((bwd_table.width() / sum(column_ratios.values())) * v * .98, 0))
#         bwd_table.setColumnWidth(k, width)
