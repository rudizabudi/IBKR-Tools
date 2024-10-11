from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QVBoxLayout,
    QWidget, QStyleOptionTab)

from PyQt5.QtWidgets import QTabWidget
from gui.tabs.beta_weighted_deltas import BetaWeightedDeltas


type CoreObj = 'CoreObj'
# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):

    def __init__(self, core: CoreObj):
        super().__init__()

        self.core = core

        self.bwd: BetaWeightedDeltas = BetaWeightedDeltas(core=self.core)

        self.core.frame_tabs = {'Beta Weighted Deltas': self.bwd,}

        self.tabs = QTabWidget()
        self.frame_box = QVBoxLayout()
        self.central_widget = QWidget()


    def create_gui(self):

        self.setWindowTitle(f'IBKR Tools')
        self.setGeometry(25, 40, 1250, 1250)

        for k in self.core.frame_tabs.keys():
            self.tabs.addTab(QWidget(), k)

        self.tabs.setStyleSheet("QTabBar::tab { height: 25px; width: 200px; font-size: 18px}")
        self.tabs.setFixedHeight(25)
        self.frame_box.addWidget(self.tabs)

        self.central_widget.setLayout(self.frame_box)
        self.setCentralWidget(self.central_widget)

        self.tabs.currentChanged.connect(self.change_tab)
        self.change_tab()

    def change_tab(self):

        tab_name = self.tabs.tabText(self.tabs.currentIndex())
        self.core.active_tab = tab_name
        tab = self.core.frame_tabs[tab_name]
        self.frame_box.addWidget(tab.get_tab_element())

        tab.update_time_now()
