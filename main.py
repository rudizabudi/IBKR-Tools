from PyQt5.QtWidgets import QApplication
from threading import Thread

import core
from gui import frame, skin
from services import controller


if __name__ == "__main__":
    start_gui = True
    start_tws = True

    core = core.Core()
    def gui():
        app = QApplication([])
        app = skin.set_skin(app)
        window = frame.MainWindow(core=core)
        window.create_gui()
        window.show()
        app.exec_()

    if start_gui:
        Thread(target=gui).start()

    def tws():
        tws_con = controller.TWSRequests(core=core)
        tws_con.control_loop()

    if start_tws:
        tws()

