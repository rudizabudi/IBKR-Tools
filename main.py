from PySide6.QtGui import QIcon
from ibapi.contract import Contract
from time import sleep
from PySide6.QtWidgets import QApplication
import sys
from threading import Thread

import core
from gui.frame import MainWindow
from services import controller


if __name__ == "__main__":
    start_gui = True
    start_tws_inst = True
    start_controller_loop = True
    tester = False

    core = core.Core()

    def gui():
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("icon.ico"))
        MainWindow(core=core)
        sys.exit(app.exec())

        # window.create_gui()
        # window.show()
        # app.exec_()

    if start_gui:
        Thread(target=gui).start()

    def tws_con():
        return controller.TWSRequests(core=core)

    if start_tws_inst:
        tws_con = tws_con()

    def tws_loop(tws_con):
        tws_con.control_loop()

    if start_controller_loop:
        tws_loop(tws_con)

    def test_lab(tws_con):
        rc = Contract()
        rc.symbol = 'SPY'
        rc.secType = 'STK'
        rc.currency = 'USD'
        rc.exchange = 'SMART'
        print(rc)
        rc2 = Contract()
        rc2.symbol = 'BMW'
        rc2.secType = 'STK'
        rc2.currency = 'EUR'
        rc2.exchange = 'IBIS'
        print(rc2)
        #tws_con.tws_api.reqFundamentalData(131 , rc, "ReportSnapshot", "")
        #tws_con.tws_api.reqContractDetails(132 , rc, "RESC", "")
        from datetime import datetime
        tws_con.tws_api.reqHistoricalData(reqId=456,
                          contract=rc2,
                          endDateTime=datetime.today().strftime("%Y%m%d-%H:%M:%S"),
                          durationStr='1 Y',
                          barSizeSetting='1 day',
                          whatToShow="MIDPOINT",
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])

        print(12354)
        sleep(999999)

    if tester:
        test_lab(tws_con)

