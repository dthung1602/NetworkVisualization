from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QCheckBox, QComboBox, QPushButton, QSlider
from PyQt5.uic import loadUi

from Canvas import Canvas
from RandomDialog import RandomDialog

TITLE = [
    'No.',
    'Key',
]

DIST = [
    'Normal distribution',
    'Uniform distribution'
]


class BuddyLabel(QLabel):
    def __init__(self, buddy, parent=None):
        super(BuddyLabel, self).__init__(parent)
        self.buddy = buddy
        self.buddy.hide()

    # When it's clicked, hide itself and show its buddy
    def mousePressEvent(self, event):
        self.hide()
        self.buddy.show()
        self.buddy.setFocus()  # Set focus on buddy so user doesn't have to click again


class RealTimeDialog(QWidget):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self.canvas = canvas
        loadUi('resource/gui/RealTimeDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Real Time Visualization Tool")
        self.labelStyleSheet = ("color: rgb(180,180,180); background-color: transparent;")
        self.checkBoxList = []
        self.vertexAttr = []
        self.edgeAttr = []
        self.attr = []
        self.generateBtn = self.findChild(QPushButton, 'generate_btn')
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
        self.selectDistribution.addItems([opt for opt in DIST])

        for i in range(len(self.checkBoxList)):
            self.checkBoxList[i].stateChanged.connect(self.checkBoxEdited)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.canvas.inRealTimeMode = False
        super().closeEvent(a0)

    def addVertexKey(self):
        count = 1
        for key in self.canvas.g.vs.attributes():
            value = self.canvas.g.vs[0][key]
            keyLabel = QLabel(key)
            keyLabel.setStyleSheet(self.labelStyleSheet)
            if isinstance(value, float) and key not in VertexKeyIgnore.ignoredFields:
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
            if isinstance(value, float) and key not in EdgeKeyIgnore.ignoredFields:
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

    def sliderValueChange(self):
        self.fPs = self.slider.value()

    def checkBoxEdited(self, state):
        if state == QtCore.Qt.Checked:
            self.openRandomDialog(self.sender().objectName())
        else:
            print('unchecked')

    def openRandomDialog(self, name):
        randomDialog = RandomDialog(self.canvas, getattr(self.sender(), "type"))
        self.setObjectName(name)
        setattr(randomDialog, "update", False)
        randomDialog.exec()
        randomDialog.attrBack.append(name)
        if getattr(self.sender(), "type").upper() == "EDGE":
            self.edgeAttr.append(randomDialog.attrBack)
        else:
            self.vertexAttr.append(randomDialog.attrBack)
        print("Sender type : ", getattr(self.sender(), "type"))
        self.notify(randomDialog.attrBack, getattr(self.sender(), "type"))
        self.notify(randomDialog.attrBack, getattr(self.sender(), "type"))

    def realTimeEvent(self):
        self.attr.append(self.vertexAttr)
        self.attr.append(self.edgeAttr)
        self.attr.append(self.fps)
        self.canvas.inRealTimeMode = True
        self.canvas.startRealTime(self.attr)
        self.notiLabel.setText("Real Time Mode: ON!")

    def notify(self, mes, type):
        dist, value1, value2, name = mes
        if type is "VERTEX":
            for r in range(1, self.vertexGridLayout.rowCount()):
                for c in range(2, self.vertexGridLayout.columnCount()):
                    item = self.vertexGridLayout.itemAtPosition(r, c)
                    if item is not None:
                        if dist == "Normal Distribution":
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value1'):
                                (item.widget()).setText("Mean = " + str(value1))
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Std = " + str(value2))
                        else:
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value1'):
                                (item.widget()).setText("Min = " + str(value1))
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Max = " + str(value2))
        else:
            for r in range(1, self.edgeGridLayout.rowCount()):
                for c in range(2, self.edgeGridLayout.columnCount()):
                    item = self.edgeGridLayout.itemAtPosition(r, c)
                    if item is not None:
                        if dist == "Normal Distribution":
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value1'):
                                (item.widget()).setText("Mean = " + str(value1))
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Std = " + str(value2))
                        else:
                            if (item.widget()).objectName() == (name + 'dist'):
                                (item.widget()).setText(dist)
                            if (item.widget()).objectName() == (name + 'value1'):
                                (item.widget()).setText("Min = " + str(value1))
                            if (item.widget()).objectName() == (name + 'value2'):
                                (item.widget()).setText("Max = " + str(value2))


class VertexKeyIgnore(RealTimeDialog):
    ignoredFields = ['hyperedge']


class EdgeKeyIgnore(RealTimeDialog):
    ignoredFields = ['b_delay', 't_delay', 'p_delay', 'key', 'zorder', 'edge_weight']
