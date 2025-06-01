import faulthandler
import sys
from threading import Thread

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from core import Core, CoreDistributor
from gui.frame import MainWindow


faulthandler.enable()


def gui():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    MainWindow()
    sys.exit(app.exec())

    # window.create_gui()
    # window.show()
    # app.exec_()

if __name__ == "__main__":
    core: Core = CoreDistributor.get_core()
    Thread(target=gui).start()


"""
TODO: Make reqIDs and req_hashtable thread-safe
TODO: Rewrite backend while loop -> thread waits
"""


"""
IDEA: Add a dollar-beta weighted column for exposure (Mark Meldrum: https://youtu.be/FYszi2Otsrw?si=K62RdfPEi0if3hC2&t=1656)
"""

