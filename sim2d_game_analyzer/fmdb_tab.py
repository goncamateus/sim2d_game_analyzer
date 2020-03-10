import pandas as pd
from PyQt5.QtCore import QEvent, QPoint, Qt
from PyQt5.QtGui import QBrush, QIcon, QPainter, QPen
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QDialogButtonBox, QFileDialog, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit, QSlider,
                             QStyleOptionSlider, QToolTip, QVBoxLayout,
                             QWidget)

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
BALL_SIZE = 0.085


class TipSlider(QSlider):
    def __init__(self, *args, tip_offset=QPoint(0, -45)):
        super(QSlider, self).__init__(*args)
        self.tip_offset = tip_offset

        self.style = QApplication.style()
        self.opt = QStyleOptionSlider()

        self.valueChanged.connect(self.show_tip)

    def show_tip(self, _):
        self.initStyleOption(self.opt)
        rectHandle = self.style.subControlRect(
            self.style.CC_Slider, self.opt, self.style.SC_SliderHandle)

        pos_local = rectHandle.topLeft() + self.tip_offset
        pos_global = self.mapToGlobal(pos_local)
        QToolTip.showText(pos_global, str(self.value()), self)


class Field(QGroupBox):
    def __init__(self, parent):
        super(Field, self).__init__("")
        self.base_data = None
        self.dbs = [None for _ in range(11)]
        self.selected_player = 1
        self.selected_class = "Good"
        self.saved_points = {kc: {key: [list() for _ in range(11)]
                                  for key in range(1, 6001)} for kc in ['Good',
                                                                        'Bad']}
        self.time = 1
        self.save_columns = []
        self.mx = 1
        self.my = 1
        self.fmid = 0
        self.ball = None
        self.players_l = [None for _ in range(11)]
        self.players_r = [None for _ in range(11)]
        self.setMouseTracking(True)

    def reset_player_at_time(self):
        self.saved_points[self.selected_class][
            self.time][self.selected_player - 1] = list()

    def reset(self):
        self.dbs = [None for _ in range(11)]
        self.saved_points = {kc: {key: [list() for _ in range(11)]
                                  for key in range(1, 6001)} for kc in ['Good',
                                                                        'Bad']}

    def set_time(self, time):
        self.time = time
        self.update()

    def set_base(self, df):
        self.base_data = df
        columns = ['show_time', 'ball_x', 'ball_y']
        player_l = ['player_lNUMBER_x'.replace(
            'NUMBER', str(num + 1)) for num in range(11)]
        player_l = player_l + ['player_lNUMBER_y'.replace(
            'NUMBER', str(num + 1)) for num in range(11)]
        player_l.sort(key=lambda x: int(x.split('_')[1][1:]))
        player_r = ['player_rNUMBER_x'.replace(
            'NUMBER', str(num + 1)) for num in range(11)]
        player_r = player_r + ['player_rNUMBER_y'.replace(
            'NUMBER', str(num + 1)) for num in range(11)]
        player_r.sort(key=lambda x: int(x.split('_')[1][1:]))
        columns = columns + player_l + player_r
        self.base_data = self.base_data[columns]
        self.time = 1
        self.update()

    def mouseMoveEvent(self, e):
        mid_x, mid_y = self.fmid
        self.mx = (e.x() - mid_x)/12
        self.my = (e.y() - mid_y)/12
        text = "{:.1f}, {:.1f}".format(self.mx, self.my)
        self.setToolTip(text)
        QToolTip.showText(QPoint(e.x(), e.y()), str(text), self)

    def mousePressEvent(self, e):
        if self.base_data is not None:
            mid_x, mid_y = self.fmid
            self.cx = (e.x() - mid_x)/12
            self.cy = (e.y() - mid_y)/12
            db = self.dbs[self.selected_player - 1]
            if db is None:
                db = list()
            at_time = self.base_data[self.base_data['show_time']
                                     == self.time].iloc[0]
            my_array = list()
            for key in at_time.keys():
                if not key in ['show_time', f'player_l{self.selected_player}_x',
                               f'player_l{self.selected_player}_y']:
                    my_array.append(at_time[key])
                elif key != 'show_time':
                    if key.endswith('x'):
                        my_array.append(self.cx)
                    else:
                        my_array.append(self.cy)
            if self.selected_class == "Good":
                my_array.append(1)
            else:
                my_array.append(0)
            db.append(my_array)
            self.save_columns = [x for x in at_time.keys() if x != 'show_time']
            self.save_columns.append('class')
            self.dbs[self.selected_player - 1] = db
            self.saved_points[self.selected_class][
                self.time][self.selected_player - 1].append((self.cx, self.cy))
            self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        field_brush = QBrush(Qt.green, Qt.SolidPattern)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setPen(QPen(Qt.white, 3, Qt.SolidLine))
        painter.setBrush(field_brush)
        self.draw_background(painter, field_brush)
        self.draw_lines(painter)
        if self.base_data is not None:
            self.draw_players(painter)
            self.draw_ball(painter)
        # if len(self.saved_points['Good'][
        #         self.time][self.selected_player - 1]) > 0:
        self.draw_saved_points(painter)

    def draw_saved_points(self, painter):
        painter.setPen(QPen(Qt.white, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        for point_x, point_y in self.saved_points['Good'][self.time][
                self.selected_player - 1]:
            painter.drawPoint(
                point_x*12 + self.fmid[0], point_y*12 + self.fmid[1])
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for point_x, point_y in self.saved_points['Bad'][self.time][
                self.selected_player - 1]:
            painter.drawPoint(
                point_x*12 + self.fmid[0], point_y*12 + self.fmid[1])

    def draw_players(self, painter):
        at_time = self.base_data[self.base_data['show_time']
                                 == self.time].iloc[0]
        # Left players
        for side, color in [('l', Qt.blue), ('r', Qt.red)]:
            for i in range(1, 12):
                if i == self.selected_player and side == 'l':
                    painter.setPen(QPen(Qt.yellow, 10, Qt.SolidLine))
                else:
                    painter.setPen(QPen(color, 10, Qt.SolidLine))
                x = at_time[f'player_{side}{i}_x']*12
                y = at_time[f'player_{side}{i}_y']*12
                x = self.fmid[0] + x
                y = self.fmid[1] + y
                painter.drawEllipse(
                    QPoint(x, y),
                    PLAYER_SIZE*12, PLAYER_SIZE*12)

    def draw_ball(self, painter):
        at_time = self.base_data[self.base_data['show_time']
                                 == self.time].iloc[0]
        x = self.fmid[0] + at_time.ball_x*12
        y = self.fmid[1] + at_time.ball_y*12
        painter.setPen(QPen(Qt.white, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        painter.drawEllipse(
            QPoint(x, y),
            PLAYER_SIZE*10, PLAYER_SIZE*10)

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
        self.db = pd.DataFrame()
        self.mainLayout = QVBoxLayout()
        self.optionsGroup = QGroupBox("")
        self.optionsLayout = QHBoxLayout()
        self.optionsGroup.setLayout(self.optionsLayout)
        self.create_class_GB()
        self.create_players_GB()
        self.create_slider()
        self.mainLayout.addWidget(self.optionsGroup)
        self.field = Field(self)
        self.mainLayout.addWidget(self.field)
        self.optionsGroup.setMaximumHeight(70)
        buttonbox = QDialogButtonBox(
            QDialogButtonBox.Open |
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel)
        buttonbox.buttons()[1].clicked.connect(self.open)
        buttonbox.buttons()[0].clicked.connect(self.save)
        buttonbox.buttons()[2].clicked.connect(self.cancel)
        self.mainLayout.addWidget(buttonbox)
        self.setLayout(self.mainLayout)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus(True)

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            base_df = pd.read_csv(fileName)
            self.field.set_base(base_df)

    def save(self):
        self.dbs = self.field.dbs
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Dataset", "",
            "All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            fileName = fileName.replace('csv', '')
            for unum, db in enumerate(self.dbs):
                name = fileName + str(unum + 1) + '.csv'
                df = pd.DataFrame(
                    db, columns=self.field.save_columns)
                df.to_csv(name, index=False)

    def cancel(self):
        self.dbs = [None for _ in range(11)]
        self.combo_classes.setCurrentText('Good')
        self.combo_players.setCurrentText('1')
        self.sld.setValue(1)
        self.field.reset()

    def reset_player_at_time(self):
        self.field.reset_player_at_time()

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
        self.sld.valueChanged.connect(
            lambda: self.field.set_time(self.sld.value()))
        self.optionsLayout.addWidget(self.sld)

    def change_class(self, value):
        self.SELECTED_CLASS = value
        self.field.selected_class = value

    def change_player(self, value):
        self.SELECTED_PLAYER = value
        self.field.selected_player = int(value)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.sld.setValue(self.sld.value() + 1)
        elif event.key() == Qt.Key_Left:
            self.sld.setValue(self.sld.value() - 1)
        elif event.key() == Qt.Key_G:
            self.combo_classes.setCurrentText('Good')
        elif event.key() == Qt.Key_B:
            self.combo_classes.setCurrentText('Bad')
        elif event.key() == 45:
            self.combo_players.setCurrentText('11')
        elif event.key() > 47 and event.key() < 58:
            num = int(event.key()) - 48
            num = num if num != 0 else 10
            self.combo_players.setCurrentText(f'{num}')
        elif event.key() == Qt.Key_Escape:
            self.cancel()
        elif event.key() == Qt.Key_O:
            self.open()
        elif event.key() == Qt.Key_S:
            self.save()
        elif event.key() == Qt.Key_R:
            self.reset_player_at_time()
        else:
            QWidget.keyPressEvent(self, event)
        self.field.set_time(self.sld.value())
