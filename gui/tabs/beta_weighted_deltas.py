from datetime import datetime
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget, QHBoxLayout, QWidget, QTableWidget, QSizePolicy, QAbstractItemView, QVBoxLayout, QLabel, QTableWidgetItem

type CoreObj = 'CoreObj'
type QtObj = 'QtObj'


class BetaWeightedDeltas:
    def __init__(self, core: CoreObj):

        self.core: CoreObj = core
        self.table_contents = core.table_contents

        self._widget_built_finished: bool = False

        self.previous_selection: None | str = None

        self.symbol_list: list = ['Loading...']

    def build_widget(self):
        def underlying_selection_list() -> QListWidget:
            list_widget = QListWidget()
            list_widget.setFont(QFont("", 18))
            list_widget.addItems(['LOADING...'])
            list_widget.setMaximumWidth(200)
            list_widget.setMinimumWidth(100)
            list_widget.setMinimumHeight(500)
            list_widget.resize(200, 1245)

            list_widget.currentItemChanged.connect(self.selection_list_change)
            self.core.item_register['underlying_selection_list'] = list_widget

            return list_widget

        def greek_table() -> QTableWidget:
            table = QTableWidget(1000, 9)
            table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            table.setMinimumSize(1020, 1230)
            headers = ['Symbol', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', ' γ Gamma (L|S)', 'Notional position']
            table.setHorizontalHeaderLabels(headers)

            table.setSelectionMode(QAbstractItemView.NoSelection)
            table.verticalHeader().setVisible(False)

            column_ratios = {0: 3,
                             1: 7,
                             2: 2,
                             3: 3,
                             4: 4,
                             5: 7,
                             6: 4,
                             7: 6,
                             8: 5}

            for k, v in column_ratios.items():
                width = int(round((table.width() / sum(column_ratios.values())) * v * .98, 0))
                table.setColumnWidth(k, width)

            self.core.item_register['greek_table'] = table
            return table

        def update_label() -> QLabel:
            label = QLabel()
            label.setFont(QFont("", 10))
            label.setText(f'Last update:  --:--')
            label.setMaximumHeight(25)

            self.core.item_register['update_label'] = label

            return label

        self.bwd_box.addWidget(underlying_selection_list(), alignment=Qt.AlignLeft)

        self.bwd_box.addLayout(self.content_box)

        self.content_box.addWidget(update_label(), alignment=Qt.AlignRight)
        self.content_box.addWidget(greek_table())

        self._widget_built_finished = True

    def tab_trigger(self):
        print('bwd tab triggered')
    def get_widget_object(self, selection_list: bool = False, greek_table: bool = False):
        if all([selection_list, greek_table]):
            raise Exception('Only one of selection_list or greek_table can be True.')
        elif selection_list:
            return self.core.widget_registry['beta_weighted_deltas']['selection_list']
        elif greek_table:
            return self.core.widget_registry['beta_weighted_deltas']['greek_table']

    def change_table_content(self):
        # TODO: Add sorting via 1 or 2 selection fields: sort by and ASC/DESC(?)
        # Alternative: Sort via column header clisk
        if self.previous_selection != self.core.item_register['underlying_selection_list'].currentItem().text():
            bwd_table = self.get_widget_object(greek_table=True)
            bwd_table.clear()

            selection = self.core.item_register['underlying_selection_list'].currentItem().text()
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

            self.previous_selection = self.core.item_register['underlying_selection_list'].currentItem().text()

    def update_time_now(self):
        self.core.item_register['update_label'].setText(f'Last update:  {datetime.now().strftime('%H:%M')}')

    def update_selection_list(self, symbol_list: list):
        bwd_selection_list = self.get_widget_object(selection_list=True)
        bwd_selection_list.clear()
        #print(f'Selection table changed with length {len(symbol_list)}')
        print(f'symbol list: {symbol_list}')
        bwd_selection_list.addItems(symbol_list)
        #self.selection_list_change()

    def selection_list_change(self):
        try:
            self.change_table_content()
        except AttributeError:
            pass

    def set_symbol_list(self, symbol_list: list):
        self.symbol_list = symbol_list




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
