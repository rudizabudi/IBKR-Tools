import faulthandler
import sys
from threading import Thread
from time import sleep

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from ibapi.contract import Contract

from core import Core, CoreDistributor
from gui.frame import MainWindow

from services.controller import Backend
from services.tws_api import TWSConDistributor

faulthandler.enable()

if __name__ == "__main__":
    core: Core = CoreDistributor.get_core()
    start_gui_cond = True
    start_backend_cond = True
    tester = False


    def gui():

        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("icon.ico"))
        MainWindow()
        sys.exit(app.exec())

        # window.create_gui()
        # window.show()
        # app.exec_()

    if start_gui_cond:
        Thread(target=gui).start()

    def start_backend():
        Backend().control_loop()

    if start_backend_cond:
        start_backend()

    def test_lab():
        tws_con = TWSConDistributor.get_con()

        rc = Contract()
        rc.symbol = 'SPX'
        rc.secType = 'IND'
        rc.currency = 'USD'
        rc.exchange = 'CBOE'
        print('In Tester')

        print(12354)
        sleep(999999)

    if tester:
        test_lab()


"""
TODO: Make reqIDs and req_hashtable thread-safe
"""


"""
IDEA: Add a dollar-beta weighted column for exposure (Mark Meldrum: https://youtu.be/FYszi2Otsrw?si=K62RdfPEi0if3hC2&t=1656)
"""

