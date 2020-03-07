import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from sim2d_game_analyzer.fmdb_tab import FMDBTab


class MainWindow(QDialog):
    title = "Sim2d Game Analyzer"
    top = 500
    left = 100
    width = 70*4
    height = 130*4

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("figures/icon.png"))
        vbox = QVBoxLayout()
        tabWidget = QTabWidget()
        # buttonbox = QDialogButtonBox(
        #     QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        # buttonbox.accepted.connect(self.save)
        # buttonbox.rejected.connect(self.reject)
        tabWidget.setFont(QtGui.QFont("Sanserif", 12))

        tabWidget.addTab(FMDBTab(), FMDBTab.NAME)
        vbox.addWidget(tabWidget)
        self.setLayout(vbox)
        self.setGeometry(self.screen().geometry())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabdialog = MainWindow()
    tabdialog.showFullScreen()
    sys.exit(app.exec())
