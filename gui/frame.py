import os
from PySide6.QtWidgets import QMainWindow, QHeaderView, QSizePolicy, QAbstractItemView

#from gui.modules.ui_functions import UIFunctions
from gui.tabs.beta_weighted_deltas import BetaWeightedDeltas
from gui.modules.ui_main import Ui_MainWindow
from gui.app_settings import Settings
from gui.tabs import beta_weighted_deltas

type CoreObj = 'CoreObj'

os.environ["QT_FONT_DPI"] = "96"

widgets = None

# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):

    def __init__(self, core: CoreObj):
        QMainWindow.__init__(self)

        self.core = core

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "IBKR Tools - GUI"
        description = "IBKR Tools - GUI"
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        UIFunctions.uiDefinitions(self)

        widgets.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.core.tab_data_registry['beta_weighted_deltas'] = BetaWeightedDeltas(self.core)

        self.show()
        self.set_active_tab('home')

        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        def event_register():
            widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
            widgets.btn_home.clicked.connect(self.buttonClick)
            widgets.btn_bwd.clicked.connect(self.buttonClick)

            widgets.bwd_listWidget.currentItemChanged.connect(lambda: self.core.tab_data_registry['beta_weighted_deltas'].change_table_content())

        event_register()

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        self.core.widget_registry = {
                'beta_weighted_deltas': {'selection_list': widgets.bwd_listWidget, 'greek_table': widgets.bwd_tableWidget},
            }

        #Tab instances
        self.core.tab_data_registry['beta_weighted_deltas'] = BetaWeightedDeltas(self.core)

        def adjust_widgets():
            def bwd_table():
                headers = ['Symbol', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', ' γ Gamma (L|S)', 'Notional position']
                widgets.bwd_tableWidget.setHorizontalHeaderLabels(headers)

                #widgets.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                widgets.bwd_tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                widgets.bwd_tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
                widgets.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

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
                    width = int(round((widgets.bwd_tableWidget.width() / sum(column_ratios.values())) * v * .96, 0))
                    widgets.bwd_tableWidget.setColumnWidth(k, width)

            bwd_table()
        adjust_widgets()

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        match btnName:
            case "btn_home":
                widgets.stackedWidget.setCurrentWidget(widgets.home)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('home')

            # SHOW WIDGETS PAGE
            case "btn_bwd":
                widgets.stackedWidget.setCurrentWidget(widgets.beta_weighted_deltas)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('beta_weighted_deltas')
                self.core.tab_data_registry['beta_weighted_deltas'].tab_trigger()

            case _:
                print(f'Unregistered button clicked: {btnName}')

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    def set_active_tab(self, tab_name):
        #print(f'Active tab: {tab_name}')
        self.core.active_tab = tab_name

from gui.modules.ui_functions import UIFunctions
