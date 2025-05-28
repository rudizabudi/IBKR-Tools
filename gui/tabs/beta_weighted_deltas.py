from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QSizePolicy, QAbstractItemView
from threading import Thread, Event

from core import Core, CoreDistributor
from services.beta_weighted_deltas.beta_weighted_deltas import UpdateSelectionList, UpdateTableGreeks


class BetaWeightedDeltas:
    def __init__(self):

        self.core: Core = CoreDistributor.get_core()
        self.table_contents = self.core.table_contents

        self.previous_selection: None | str = None

        self.tab_trigger = {'selection_list': UpdateSelectionList(),
                            'table_greeks': UpdateTableGreeks()}

        self.tab_registry = self.core.widget_registry['beta_weighted_deltas']

        self.handle_widgets()

        self.register_events()

    def register_events(self):
        self.tab_registry['list_selection'].currentItemChanged.connect(lambda: self.change_table_content())
        self.tab_trigger['selection_list'].trigger_selection_list_update.connect(self.refresh_selection_list)
        self.tab_trigger['table_greeks'].trigger_table_update.connect(self.change_table_content)

    def init_activity(self):
        print('BWD init act')
        print(self.core.backend.beta_weighted_deltas)
        self.refresh_selection_list(['Loading...'])
        t = Thread(target=self.core.backend.beta_weighted_deltas, daemon=True)
        t.start()

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

        selected_underlying = self.tab_registry['list_selection'].currentItem().text()

        bwd_table = self.tab_registry['table_greeks']
        bwd_table.clear()

        if selected_underlying not in self.core.table_contents.keys():
            raise RuntimeError(f'Selected underlying {selected_underlying} not found in table contents')

        for i, x in enumerate(self.table_contents[selected_underlying]):
            for j, y in enumerate(self.table_contents[selected_underlying][i]):  # columns
                if not y:
                    y = ''

                item = QTableWidgetItem(str(y))
                #if i in (0,) and selected_underlying not in ['Overview', 'Portfolio']:

                if j in (8,):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif j in (1, 2, 3, 4, 5, 6, 7):
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

                item.setFont(QFont(self.core.project_font, 12))
                bwd_table.setItem(i, j, item)

        headers = ['Symbol', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', 'γ Gamma (L|S)', 'Notional position']
        bwd_table.setHorizontalHeaderLabels(headers)
        bwd_table.horizontalHeader().setFont(QFont(self.core.project_font, 9))

    def refresh_selection_list(self, symbol_list: list[str]):
        input_widgets = (self.tab_registry['list_selection'], self.tab_registry['table_greeks'])
        tmp_blocked_events = [x.blockSignals(True) for x in input_widgets]

        current_item_obj = self.tab_registry['list_selection'].currentItem()
        if current_item_obj:
            selected_underlying_text = current_item_obj.text()
        else:
            selected_underlying_text = ''

        self.tab_registry['list_selection'].clear()
        self.tab_registry['list_selection'].addItems(symbol_list)

        found_previous_selection = False
        for i in range(self.tab_registry['list_selection'].count()):
            item = self.tab_registry['list_selection'].item(i)
            if item.text() == selected_underlying_text:
                self.tab_registry['list_selection'].setCurrentItem(item)
                found_previous_selection = True
                break

        if not found_previous_selection:
            if self.tab_registry['list_selection'].count() > 0:
                self.tab_registry['list_selection'].setCurrentRow(0)

        for widget, block in zip(input_widgets, tmp_blocked_events):
            widget.blockSignals(block)

        if isinstance(self.core.threading_events.get('bwd_list_updating'), Event) and not self.core.threading_events.get('bwd_list_updating').is_set():
            self.core.threading_events['bwd_list_updating'].set()
        # for i in range(selection_list.count()):
        #     selection_list.item(i).setFont(QFont(self.core.project_font, 16))





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
