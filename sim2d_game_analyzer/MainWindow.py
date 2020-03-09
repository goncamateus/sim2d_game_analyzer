import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QPoint, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QGroupBox, QMainWindow,
                             QTabWidget, QVBoxLayout, QWidget)

from sim2d_game_analyzer.fmdb_tab import FMDBTab


class MainWindow(QMainWindow):
    title = "Sim2d Game Analyzer"
    top = 500
    left = 100
    width = 70*4
    height = 130*4

    def __init__(self):
        QMainWindow.__init__(self)
        self.setGeometry(self.screen().geometry())
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("sim2d_game_analyzer/figures/icon.png"))
        vbox = QVBoxLayout()
        tabWidget = QTabWidget()

        tabWidget.setFont(QtGui.QFont("Sanserif", 12))
        self.fmdb_tab = FMDBTab()
        tabWidget.addTab(self.fmdb_tab, FMDBTab.NAME)
        vbox.addWidget(tabWidget)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())
