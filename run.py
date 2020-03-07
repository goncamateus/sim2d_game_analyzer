import sys

from PyQt5.QtWidgets import QApplication

from sim2d_game_analyzer.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tabdialog = MainWindow()
    tabdialog.show()
    sys.exit(app.exec())
