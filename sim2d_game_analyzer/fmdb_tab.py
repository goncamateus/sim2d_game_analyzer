from PyQt5.QtCore import QEvent, QPoint, Qt
from PyQt5.QtGui import QBrush, QIcon, QPainter, QPen
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
                             QLineEdit, QSlider, QStyleOptionSlider, QToolTip,
                             QVBoxLayout, QWidget)

PITCH_LENGHT = 105.0
PITCH_WIDTH = 68.0
GOAL_AREA_LENGTH = 5.5
GOAL_AREA_WIDTH = 18.32
PENALTY_AREA_LENGTH = 16.5
PENALTY_AREA_WIDTH = 40.32
CORNER_ARC_R = 1.0
PENALTY_CIRCLE_R = 9.15
PENALTY_SPOT_DIST = 11.0
PLAYER_SIZE = 0.3


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


class Field(QGroupBox):
    def __init__(self):
        super(Field, self).__init__("")
        self.mx = 1
        self.my = 1
        self.fmid = 0
        self.ball = None
        self.players_l = [None for _ in range(11)]
        self.players_r = [None for _ in range(11)]
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        mid_x, mid_y = self.fmid
        self.mx = (e.x() - mid_x)/12
        self.my = (e.y() - mid_y)/12
        text = "{:.1f}, {:.1f}".format(self.mx, self.my)
        self.setToolTip(text)
        QToolTip.showText(QPoint(e.x(), e.y()), str(text), self)

    def paintEvent(self, e):
        painter = QPainter(self)
        field_brush = QBrush(Qt.green, Qt.SolidPattern)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        painter.setBrush(field_brush)
        self.draw_background(painter, field_brush)
        self.draw_lines(painter)

    def draw_background(self, painter, field_brush):
        painter.fillRect(painter.window(), field_brush)

    def draw_lines(self, painter):
        # BOUND
        top = (painter.window().height() - PITCH_WIDTH*12)/2
        left = (painter.window().width() - PITCH_LENGHT*12)/2
        mid_height = top + PITCH_WIDTH*6
        mid_width = left + PITCH_LENGHT*6
        self.fmid = (mid_width, mid_height)
        painter.drawRect(left, top, PITCH_LENGHT*12, PITCH_WIDTH*12)
        # MID LINES
        painter.drawEllipse(QPoint(mid_width, mid_height), 9*12, 9*12)
        painter.drawLine(left + PITCH_LENGHT*6, top, left +
                         PITCH_LENGHT*6, top + PITCH_WIDTH*12)
        # painter.drawLine(left, mid_height, left + PITCH_LENGHT*12, mid_height)

        # PENALTY AREA
        painter.drawEllipse(QPoint(left + PENALTY_SPOT_DIST*12, mid_height),
                            PENALTY_CIRCLE_R*12, PENALTY_CIRCLE_R*12)
        painter.drawEllipse(QPoint(left + PITCH_LENGHT*12 - PENALTY_SPOT_DIST*12,
                                   mid_height), PENALTY_CIRCLE_R*12,
                            PENALTY_CIRCLE_R*12)
        Ptop = mid_height - PENALTY_AREA_WIDTH*6
        painter.drawRect(left, Ptop, PENALTY_AREA_LENGTH *
                         12, PENALTY_AREA_WIDTH*12)
        painter.drawRect(left + PITCH_LENGHT*12 - PENALTY_AREA_LENGTH*12, Ptop,
                         PENALTY_AREA_LENGTH*12, PENALTY_AREA_WIDTH*12)
        # GOAL
        Gtop = mid_height - GOAL_AREA_WIDTH*6
        painter.drawRect(left, Gtop, GOAL_AREA_LENGTH*12, GOAL_AREA_WIDTH*12)
        painter.drawRect(left + PITCH_LENGHT*12 - GOAL_AREA_LENGTH*12, Gtop,
                         GOAL_AREA_LENGTH*12, GOAL_AREA_WIDTH*12)


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
        self.create_slider()
        self.mainLayout.addWidget(self.optionsGroup)
        self.field = Field()
        self.mainLayout.addWidget(self.field)
        self.optionsGroup.setMaximumHeight(70)
        buttonbox = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.save)
        buttonbox.rejected.connect(self.cancel)
        self.mainLayout.addWidget(buttonbox)
        self.setLayout(self.mainLayout)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus(True)

    def save(self):
        pass

    def cancel(self):
        pass

    def create_class_GB(self):
        my_list = ["Good", "Bad"]
        self.combo_classes = QComboBox()
        self.combo_classes.addItems(my_list)
        self.combo_classes.currentTextChanged.connect(self.change_class)
        self.optionsLayout.addWidget(self.combo_classes)

    def create_players_GB(self):
        my_list = [str(i) for i in range(1, 12)]
        self.combo_players = QComboBox()
        self.combo_players.addItems(my_list)
        self.combo_players.currentTextChanged.connect(self.change_player)
        self.optionsLayout.addWidget(self.combo_players)

    def create_slider(self):
        self.sld = TipSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.StrongFocus)
        self.sld.setRange(1, 6000)
        self.sld.setValue(1)
        self.sld.setGeometry(325, 20, PITCH_LENGHT*9, 20)
        self.sld.setTickInterval(100)
        self.sld.setTickPosition(QSlider.TicksBelow)
        self.optionsLayout.addWidget(self.sld)

    def change_class(self, value):
        self.SELECTED_CLASS = value

    def change_player(self, value):
        self.SELECTED_PLAYER = value

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.sld.setValue(self.sld.value() + 1)
        elif event.key() == Qt.Key_Left:
            self.sld.setValue(self.sld.value() - 1)
        else:
            QWidget.keyPressEvent(self, event)
