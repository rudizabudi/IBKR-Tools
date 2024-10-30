import os
from PySide6.QtWidgets import QMainWindow, QHeaderView

#from gui.modules.ui_functions import UIFunctions
from gui.tabs.beta_weighted_deltas import BetaWeightedDeltas
from gui.modules.ui_main import Ui_MainWindow
from gui.app_settings import Settings
type CoreObj = 'CoreObj'

os.environ["QT_FONT_DPI"] = "96"

widgets = None

# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):

    def __init__(self, core: CoreObj):
        QMainWindow.__init__(self)

        #self.core = core
        #
        # self.bwd: BetaWeightedDeltas = BetaWeightedDeltas(core=self.core)

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

        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        from gui.modules.ui_functions import UIFunctions
        UIFunctions.uiDefinitions(self)

        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # CLICK EVENTS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)

        self.show()

        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        match btnName:
            case "btn_home":
                widgets.stackedWidget.setCurrentWidget(widgets.home)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            # SHOW WIDGETS PAGE
            case "btn_widgets":
                widgets.stackedWidget.setCurrentWidget(widgets.beta_weighted_deltas)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            # SHOW NEW PAGE
            case "btn_new":
                widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
                UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

            case _:
                ...

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')