from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QCheckBox, QComboBox, QPushButton, QSlider
from PyQt5.uic import loadUi
import re
from canvas import Canvas, RealTimeMode
from .RealTimeRandomDialog import RealTimeRandomDialog

DIST = [
    'Normal distribution',
    'Uniform distribution'
]
VERTEX_IGNORED_KEYS = ['hyperedge']

EDGE_IGNORED_KEYS = ['b_delay', 't_delay', 'p_delay', 'key', 'zorder', 'edge_weight']


class RealTimeDialog(QWidget):
    def __init__(self, canvas: Canvas, realtimeMode: RealTimeMode):
        super().__init__()
        self.canvas = canvas
        self.realtimeMode = realtimeMode
        self.count = 0
        loadUi('resource/gui/RealTimeDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Real Time Visualization Tool")
        self.labelStyleSheet = "color: rgb(180,180,180); background-color: transparent;"
        self.checkBoxList = []
        self.vertexAttr = []
        self.edgeAttr = []
        self.attr = []
        self.generateBtn = self.findChild(QPushButton, 'generate_btn')
        self.generateBtn.setEnabled(False)
        self.generateBtn.pressed.connect(self.realTimeEvent)
        self.notiLabel = self.findChild(QLabel, 'notiLabel')
        # FPS
        self.fpsSlider = self.findChild(QSlider, 'fpsSlider')
        self.fpsSlider.setMinimum(10)
        self.fpsSlider.setMaximum(50)
        self.fpsSlider.setValue(30)
        self.fps = 30
        self.fpsSlider.setTickPosition(QSlider.TicksBelow)
        self.fpsSlider.setTickInterval(5)
        self.fpsValueLabel = self.findChild(QLabel, 'fpsLabel')
        self.fpsSlider.valueChanged.connect(self.changeFPSValue)
        # Vertex tab
        self.vertexGridLayout = self.findChild(QGridLayout, 'vertexGridLayout')
        self.edgeGridLayout = self.findChild(QGridLayout, 'edgeGridLayout')
        self.addVertexKey()
        self.addEdgeKey()
        self.selectDistribution = QComboBox()

        self.selectDistribution.addItems(DIST)

        for i in range(len(self.checkBoxList)):
            self.checkBoxList[i].stateChanged.connect(self.checkBoxEdited)

    def closeEvent(self, event):
        self.canvas.removeMode(self.realtimeMode)
        super().closeEvent(event)

    def addVertexKey(self):
        count = 1
        for key in self.canvas.g.vs.attributes():
            value = self.canvas.g.vs[0][key]
            keyLabel = QLabel(key)
            keyLabel.setStyleSheet(self.labelStyleSheet)
            if isinstance(value, float) and key not in VERTEX_IGNORED_KEYS:
                self.vertexGridLayout.addWidget(keyLabel, count, 0)
                checkBox = QCheckBox(self)
                checkBox.setStyleSheet("QCheckBox{   border: none; color: red;}")
                checkBox.setObjectName(key)
                setattr(checkBox, "type", "VERTEX")
                self.checkBoxList.append(checkBox)
                self.vertexGridLayout.addWidget(checkBox, count, 1)
                distLabel = QLabel("None")
                distLabel.setObjectName(key + 'dist')
                distLabel.setStyleSheet(self.labelStyleSheet)
                self.vertexGridLayout.addWidget(distLabel, count, 2)
                firstValueLabel = QLabel("None")
                firstValueLabel.setObjectName(key + 'value1')
                firstValueLabel.setStyleSheet(self.labelStyleSheet)
                self.vertexGridLayout.addWidget(firstValueLabel, count, 3)
                secondValueLabel = QLabel("None")
                secondValueLabel.setObjectName(key + 'value2')
                secondValueLabel.setStyleSheet(self.labelStyleSheet)
                self.vertexGridLayout.addWidget(secondValueLabel, count, 4)

                count += 1

    def changeFPSValue(self):
        fpsValue = self.fpsSlider.value()
        self.fpsValueLabel.setText('FPS Value = ' + str(fpsValue))
        self.fps = fpsValue

    # self.selectDistribution.currentIndexChanged.connect(self.changeDist)
    def addEdgeKey(self):
        count = 1
        for key in self.canvas.g.es.attributes():
            value = self.canvas.g.es[0][key]
            keyLabel = QLabel(key)
            keyLabel.setStyleSheet(self.labelStyleSheet)
            if isinstance(value, float) and key not in EDGE_IGNORED_KEYS:
                self.edgeGridLayout.addWidget(keyLabel, count, 0)
                checkBox = QCheckBox(self)
                checkBox.setObjectName(key)
                setattr(checkBox, "type", "EDGE")
                self.checkBoxList.append(checkBox)
                self.edgeGridLayout.addWidget(checkBox, count, 1)
                distLabel = QLabel("None")
                distLabel.setObjectName(key + 'dist')
                distLabel.setStyleSheet(self.labelStyleSheet)
                self.edgeGridLayout.addWidget(distLabel, count, 2)
                firstValueLabel = QLabel("None")
                firstValueLabel.setObjectName(key + 'value1')
                firstValueLabel.setStyleSheet(self.labelStyleSheet)
                self.edgeGridLayout.addWidget(firstValueLabel, count, 3)
                secondValueLabel = QLabel("None")
                secondValueLabel.setObjectName(key + 'value2')
                secondValueLabel.setStyleSheet(self.labelStyleSheet)
                self.edgeGridLayout.addWidget(secondValueLabel, count, 4)
                count += 1

    def checkBoxEdited(self, state):

        try:
            if state == QtCore.Qt.Checked:
                self.openRandomDialog(self.sender().objectName())
            else:
                if (getattr(self.sender(), "VERTEX")):
                    row = self.vertexGridLayout.getItemPosition(self.vertexGridLayout.indexOf(self.sender()))[0]
                    col = self.vertexGridLayout.getItemPosition(self.vertexGridLayout.indexOf(self.sender()))[1]
                    dist = self.vertexGridLayout.itemAtPosition(row, col + 1).widget().text()
                    value = self.vertexGridLayout.itemAtPosition(row, col + 3).widget().text()
                    res = float(re.findall("\d+\.\d+", value)[0])
                    vertexToRemove = [dist, res, self.sender().objectName()]
                    self.vertexAttr.remove(vertexToRemove)
                    print(self.vertexAttr)
                    print(vertexToRemove)
                else:
                    row = self.vertexGridLayout.getItemPosition(self.vertexGridLayout.indexOf(self.sender()))[0]
                    col = self.vertexGridLayout.getItemPosition(self.vertexGridLayout.indexOf(self.sender()))[1]
                    dist = self.vertexGridLayout.itemAtPosition(row, col + 1).widget().text()
                    value = self.vertexGridLayout.itemAtPosition(row, col + 3).widget().text()
                    res = float(re.findall("\d+\.\d+", value)[0])
                    vertexToRemove = [dist, res, self.sender().objectName()]
                    self.edgeAttr.remove(vertexToRemove)
                    print(self.edgeAttr)
                    print(vertexToRemove)
                self.count -= 1
            if self.count == 0:
                self.generateBtn.setEnabled(False)
        except Exception as e:
            print(e.__traceback__.tb_lineno, " ", e)

    def openRandomDialog(self, name):

        try:
            randomDialog = RealTimeRandomDialog(self.canvas, getattr(self.sender(), "type"))
            self.setObjectName(name)
            setattr(randomDialog, "update", False)
            randomDialog.exec()
            randomDialog.attrBack.append(name)
            if getattr(self.sender(), "type").upper() == "EDGE":
                self.edgeAttr.append(randomDialog.attrBack)
                if len(randomDialog.attrBack) == 3:
                    self.count += 1
                    self.notify(randomDialog.attrBack, getattr(self.sender(), "type"))
                else:
                    self.count-=1
            else:
                self.vertexAttr.append(randomDialog.attrBack)
                if len(randomDialog.attrBack) == 3:
                    self.count += 1
                    self.notify(randomDialog.attrBack, getattr(self.sender(), "type"))
                else:
                    self.count-=1
            if self.count > 0:
                print("Checkin")
                self.generateBtn.setEnabled(True)
            print(self.count)
        except Exception as e:
            print(e.__traceback__.tb_lineno, " ", e)

    def realTimeEvent(self):
        self.realtimeMode.vertexAttr = self.vertexAttr
        self.realtimeMode.edgeAttr = self.edgeAttr
        self.realtimeMode.fps = self.fps
        self.canvas.addMode(self.realtimeMode)
        self.notiLabel.setText("Real Time Mode: ON!")

    def notify(self, mes, type):
        print(mes)
        dist, value2, name = mes
        if type is "VERTEX":
            for r in range(1, self.vertexGridLayout.rowCount()):
                for c in range(2, self.vertexGridLayout.columnCount()):
                    item = self.vertexGridLayout.itemAtPosition(r, c)
                    if item is not None:
                        if dist == "Normal Distribution":
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Std = " + str(value2))
                        else:
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Interval = " + str(value2))
        else:
            for r in range(1, self.edgeGridLayout.rowCount()):
                for c in range(2, self.edgeGridLayout.columnCount()):
                    item = self.edgeGridLayout.itemAtPosition(r, c)
                    if item is not None:
                        if dist == "Normal Distribution":
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Std = " + str(value2))
                        else:
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Interval = " + str(value2))
