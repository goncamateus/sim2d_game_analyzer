from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QStyleOptionSlider
from PyQt5.QtWidgets import QToolTip
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class TipSlider(QSlider):
    def __init__(self, *args, tip_offset=QPoint(0, -45)):
        super(QSlider, self).__init__(*args)
        self.tip_offset = tip_offset

        self.style = QApplication.style()
        self.opt = QStyleOptionSlider()

        self.valueChanged.connect(self.show_tip)
        # self.enterEvent = self.show_tip
        # self.mouseReleaseEvent = self.show_tip

    def show_tip(self, _):
        self.initStyleOption(self.opt)
        rectHandle = self.style.subControlRect(
            self.style.CC_Slider, self.opt, self.style.SC_SliderHandle)

        pos_local = rectHandle.topLeft() + self.tip_offset
        pos_global = self.mapToGlobal(pos_local)
        QToolTip.showText(pos_global, str(self.value()), self)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Left, Qt.Key_Right]:
            if event.key() == Qt.Key_Left and self.value() > self.minimum():
                self.setValue(self.value() - 1)
            elif event.key() == Qt.Key_Right and self.value() < self.maximum():
                self.setValue(self.value() + 1)
        else:
            super().keyPressEvent(event)


class Field(QGroupBox):
    def __init__(self):
        super(Field, self).__init__("")
        self.create_slider()

    def create_slider(self):
        sld = TipSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(1, 6000)
        sld.setValue(1)
        sld.setGeometry(325, 20, 1300, 20)
        sld.setTickInterval(100)
        sld.setTickPosition(QSlider.TicksBelow)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        painter.drawRect(325, 50, 1300, 650)


class FMDBTab(QWidget):

    NAME = "FMDB Creator"
    SELECTED_PLAYER = "1"
    SELECTED_CLASS = "Good"

    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.optionsGroup = QGroupBox("")
        self.optionsLayout = QHBoxLayout()
        self.optionsGroup.setLayout(self.optionsLayout)
        self.create_class_GB()
        self.create_players_GB()
        self.mainLayout.addWidget(self.optionsGroup)
        self.field = Field()
        self.mainLayout.addWidget(self.field)
        self.optionsGroup.setFixedHeight(200)
        buttonbox = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.save)
        buttonbox.rejected.connect(self.cancel)
        self.mainLayout.addWidget(buttonbox)
        self.setLayout(self.mainLayout)

    def save(self):
        pass

    def cancel(self):
        pass

    def create_class_GB(self):
        self.class_GB = QGroupBox("Class")
        self.class_layout = QVBoxLayout()
        my_list = ["Good", "Bad"]
        self.combo_classes = QComboBox()
        self.combo_classes.addItems(my_list)
        self.combo_classes.currentTextChanged.connect(self.change_class)
        self.class_GB.setLayout(self.class_layout)
        self.class_layout.addWidget(self.combo_classes)
        self.optionsLayout.addWidget(self.class_GB)

    def create_players_GB(self):
        self.player_GB = QGroupBox("Player")
        self.player_layout = QVBoxLayout()
        my_list = [str(i) for i in range(1, 12)]
        self.combo_players = QComboBox()
        self.combo_players.addItems(my_list)
        self.combo_players.currentTextChanged.connect(self.change_player)
        self.player_GB.setLayout(self.player_layout)
        self.player_layout.addWidget(self.combo_players)
        self.optionsLayout.addWidget(self.player_GB)

    def change_class(self, value):
        self.SELECTED_CLASS = value

    def change_player(self, value):
        self.SELECTED_PLAYER = value
