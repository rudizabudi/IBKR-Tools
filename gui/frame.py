import os

from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QMainWindow, QHeaderView, QSizePolicy, QAbstractItemView, QTableWidgetItem

from core import Core, CoreDistributor
from gui.app_settings import Settings
#from gui.modules.ui_main import Ui_MainWindow
from gui.ui_main import Ui_MainWindow
from gui.tabs.beta_weighted_deltas import BetaWeightedDeltas
from gui.tabs.box_spread import BoxSpread
from gui.font_factory import font_factory

os.environ["QT_FONT_DPI"] = "96"

widgets = None


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.core: Core = CoreDistributor.get_core()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        self.setWindowTitle("IBKR Tools")

        UIFunctions.uiDefinitions(self)

        use_custom_theme = False
        if use_custom_theme:
            theme_file = "themes\py_dracula_light.qss"
            UIFunctions.theme(self, theme_file, True)
            AppFunctions.setThemeHack(self)

        self.register_widgets()

        self.register_events()
        self.register_subpage_instances()

        self.ui.stackedWidget.setCurrentWidget(self.core.tab_instances['home'])

        self.customize_widgets()
        font_factory(core=self.core)
        self.show()
        self.set_active_tab('home')

    # Shared button registry
    def register_events(self):
        # TOGGLE MENU
        self.core.widget_registry['general']['btn_toggle'].clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        #Menu buttons
        self.core.widget_registry['general']['btn_home'].clicked.connect(self.click_handler)
        self.core.widget_registry['general']['btn_bwd'].clicked.connect(self.click_handler)
        self.core.widget_registry['general']['btn_box_spread'].clicked.connect(self.click_handler)

        #self.ui.bwd_listWidget.currentItemChanged.connect(lambda: self.core.tab_instances['beta_weighted_deltas'].change_table_content())

    # Global widget registry
    def register_widgets(self):
        self.core.widget_registry = {
                'general': {'btn_home': self.ui.btn_home, 'btn_bwd': self.ui.btn_bwd, 'btn_box_spread': self.ui.btn_box_spread, 'btn_toggle': self.ui.toggleButton,
                            'stacked_widget': self.ui.stackedWidget, 'label_header': self.ui.label_header},
                'beta_weighted_deltas': {'frame': self.ui.bwd_frame, 'list_selection': self.ui.bwd_listWidget,
                                         'table_greeks': self.ui.bwd_tableWidget},
                'box_spread':   {'btn_type': self.ui.bxs_btn_type,
                                 'label_currency': self.ui.bxs_label_currency, 'comboBox_currency': self.ui.bxs_comboBox_currency,
                                 'comboBox_index': self.ui.bxs_comboBox_index, 'label_index': self.ui.bxs_label_index,
                                 'comboBox_expiry': self.ui.bxs_comboBox_expiry, 'label_expiry': self.ui.bxs_label_expiry,
                                 'slider_rate': self.ui.bxs_horizontalSlider_rate},
                'misc': {'title_right_info': self.ui.titleRightInfo, 'leftMenuBg': self.ui.leftMenuBg, 'contentTopBg': self.ui.contentTopBg,}
            }

    # Subpage instances
    def register_subpage_instances(self):
        # Tab instances
        self.core.tab_instances['home'] = self.ui.home
        self.core.tab_instances['beta_weighted_deltas'] = BetaWeightedDeltas()
        self.core.tab_instances['box_spread'] = BoxSpread()

    # Framework widgets only
    def customize_widgets(self):
        self.core.widget_registry['general']['btn_home'].setStyleSheet(UIFunctions.selectMenu(self.core.widget_registry['general']['btn_home'].styleSheet()))

        #self.ui.titleRightInfo.setText('Title right info')
        self.core.widget_registry['general']['label_header'].setText('IBKR Tools')

        self.ui.bwd_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Shared click event handler
    def click_handler(self):
        btn = self.sender()
        btn_name = btn.objectName()

        stacked_widget = self.core.widget_registry['general']['stacked_widget']
        match btn_name:
            # Home tab
            case "btn_home":
                stacked_widget.setCurrentWidget(self.ui.home)
                UIFunctions.resetStyle(self, btn_name)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('home')

            # BWD widget tab
            case "btn_bwd":
                stacked_widget.setCurrentWidget(self.ui.beta_weighted_deltas)
                UIFunctions.resetStyle(self, btn_name)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('beta_weighted_deltas')
                #self.core.tab_instances['beta_weighted_deltas'].tab_trigger()

            # Box Spread tab
            case "btn_box_spread":
                stacked_widget.setCurrentWidget(self.ui.box_spread)
                UIFunctions.resetStyle(self, btn_name)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
                self.set_active_tab('box_spread')

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
        super().resizeEvent(event)

        match self.core.active_tab:
            case 'beta_weighted_deltas':
                self.core.tab_instances['beta_weighted_deltas'].bwd_resize_event(new_size)

from gui.modules.ui_functions import UIFunctions

