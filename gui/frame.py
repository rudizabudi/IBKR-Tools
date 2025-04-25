import os

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QMainWindow, QHeaderView, QSizePolicy, QAbstractItemView, QTableWidgetItem

from core import Core, CoreDistributor
from gui.app_settings import Settings
from gui.modules.ui_main import Ui_MainWindow
from gui.tabs.beta_weighted_deltas import BetaWeightedDeltas

os.environ["QT_FONT_DPI"] = "96"

widgets = None


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    """
    Main Window frame
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.core: Core = CoreDistributor.get_core()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        self.setWindowTitle("IBKR Tools")

        self.ui.titleRightInfo.setText('')
        self.ui.last_udpate_label.setText('IBKR Tools - GUI')
        UIFunctions.uiDefinitions(self)

        self.ui.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.set_fonts()

        self.ui.btn_home.setStyleSheet(UIFunctions.selectMenu(self.ui.btn_home.styleSheet()))

        self.register_button_clicks()
        self.register_widgets()
        self.register_subpage_instances()

        self.show()
        self.set_active_tab('home')

    def register_button_clicks(self):
        # TOGGLE MENU
        self.ui.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        #Menu buttons
        self.ui.btn_home.clicked.connect(self.click_logic)
        self.ui.btn_bwd.clicked.connect(self.click_logic)

        #self.ui.bwd_listWidget.currentItemChanged.connect(lambda: self.core.tab_instances['beta_weighted_deltas'].change_table_content())

    def register_widgets(self):
        print('Widged registered')
        self.core.widget_registry = {
                'beta_weighted_deltas': {'selection_list': self.ui.bwd_listWidget, 'greek_table': self.ui.bwd_tableWidget},
            }

    def register_subpage_instances(self):
        # Tab instances
        self.core.tab_instances['beta_weighted_deltas'] = BetaWeightedDeltas()

    def adjust_widgets(self):
        def bwd_table():
            print(f'bwd_table widget adjusted')
            headers = ['Symbol', 'β Beta / Position', 'Qty', 'iVol', 'δ Delta', 'Beta weighted deltas', 'θ  Theta', ' γ Gamma (L|S)', 'Notional position']
            self.ui.bwd_tableWidget.setHorizontalHeaderLabels(headers)

            self.ui.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.ui.bwd_tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.ui.bwd_tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
            self.ui.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

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
                width = int(round((self.ui.bwd_tableWidget.width() / sum(column_ratios.values())) * v * .96, 0))
                self.ui.bwd_tableWidget.setColumnWidth(k, width)

            self.ui.bwd_tableWidget.horizontalHeader().setFont(QFont(self.core.project_font, 9))

            for _ in range(998):
                row_position = self.ui.bwd_tableWidget.rowCount()
                self.ui.bwd_tableWidget.insertRow(row_position)

                for column in range(self.ui.bwd_tableWidget.columnCount()):
                    self.ui.bwd_tableWidget.setItem(row_position, column, QTableWidgetItem(''))

        bwd_table()

    def set_fonts(self):
        font_id = QFontDatabase.addApplicationFont(os.path.join(os.getcwd(), 'gui\\fonts\\Aquire-BW0ox.otf'))
        if font_id == -1:
            raise Exception("Failed to load the custom font.")
        else:
            self.core.project_font = QFontDatabase.applicationFontFamilies(font_id)[0]

        #self.setFont(QFont(self.core.project_font, 12))

        self.ui.titleRightInfo.setFont(QFont(self.core.project_font, 12))
        self.ui.last_udpate_label.setFont(QFont(self.core.project_font, 12))
        self.ui.btn_home.setFont(QFont(self.core.project_font, 8))
        self.ui.btn_bwd.setFont(QFont(self.core.project_font, 8))
        self.ui.toggleButton.setFont(QFont(self.core.project_font, 8))


    def click_logic(self):
        btn = self.sender()
        btn_name = btn.objectName()

        match btn_name:
            # HOme tab
            case "btn_home":
                self.ui.stackedWidget.setCurrentWidget(self.ui.home)
                UIFunctions.resetStyle(self, btn_name)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('home')

            # BWD widget tab
            case "btn_bwd":
                self.ui.stackedWidget.setCurrentWidget(self.ui.beta_weighted_deltas)
                UIFunctions.resetStyle(self, btn_name)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('beta_weighted_deltas')
                self.core.tab_instances['beta_weighted_deltas'].tab_trigger()

            case _:
                print(f'Unregistered button clicked: {btn_name}')


    def set_active_tab(self, tab_name):
        self.core.active_tab = tab_name

    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        # if event.buttons() == Qt.LeftButton:
        #     print('Mouse click: LEFT CLICK')
        # if event.buttons() == Qt.RightButton:
        #     print('Mouse click: RIGHT CLICK')

    # def resizeEvent(self, event):
    #     new_size = event.size()
    #     print(f"Window resized: {new_size.width()} x {new_size.height()}")
    #     super().resizeEvent(event)

    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)
        new_size = event.size()

        self.ui.bwd_frame.setGeometry(self.ui.bwd_frame.geometry().x(), self.ui.bwd_frame.geometry().y(), new_size.width() - self.ui.leftMenuBg.width(), new_size.height() - self.ui.contentTopBg.height())
        self.adjust_widgets()

from gui.modules.ui_functions import UIFunctions
