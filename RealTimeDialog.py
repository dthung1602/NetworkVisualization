from PyQt5 import QtCore
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
        print('Real Time Dialog')
        self.canvas = canvas
        loadUi('resource/gui/RealTimeDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Real Time Visualization Tool")
        self.checkBoxList = []
        self.attr = []
        self.generateBtn = self.findChild(QPushButton, 'generate_btn')
        self.generateBtn.pressed.connect(self.realTimeEvent)

        # FPS
        self.fpsSlider = self.findChild(QSlider, 'fpsSlider')
        self.fpsSlider.setMinimum(10)
        self.fpsSlider.setMaximum(50)
        self.fpsSlider.setValue(30)
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

    def addVertexKey(self):
        count = 1
        for key in self.canvas.g.vs.attributes():
            value = self.canvas.g.vs[0][key]
            keyLabel = QLabel(key)
            if isinstance(value, float) and key not in VertexKeyIgnore.ignoredFields:
                self.vertexGridLayout.addWidget(keyLabel, count, 0)
                checkBox = QCheckBox(self)
                checkBox.setObjectName(key)
                self.checkBoxList.append(checkBox)
                self.vertexGridLayout.addWidget(checkBox, count, 1)
                distLabel = QLabel("None")
                distLabel.setObjectName(key + 'dist')
                self.vertexGridLayout.addWidget(distLabel, count, 2)
                firstValueLabel = QLabel("None")
                firstValueLabel.setObjectName(key + 'value1')
                self.vertexGridLayout.addWidget(firstValueLabel, count, 3)
                secondValueLabel = QLabel("None")
                secondValueLabel.setObjectName(key + 'value2')
                self.vertexGridLayout.addWidget(secondValueLabel, count, 4)

                count += 1

    def changeFPSValue(self):
        fpsValue = self.fpsSlider.value()
        self.fpsValueLabel.setText('FPS Value = ' + str(fpsValue))

    # self.selectDistribution.currentIndexChanged.connect(self.changeDist)
    def addEdgeKey(self):
        count = 1
        for key in self.canvas.g.es.attributes():
            value = self.canvas.g.es[0][key]
            keyLabel = QLabel(key)
            if isinstance(value, float) and key not in EdgeKeyIgnore.ignoredFields:
                self.edgeGridLayout.addWidget(keyLabel, count, 0)
                checkBox = QCheckBox(self)
                checkBox.setObjectName(key)
                self.checkBoxList.append(checkBox)
                self.edgeGridLayout.addWidget(checkBox, count, 1)
                distLabel = QLabel("None")
                distLabel.setObjectName(key + 'dist')
                self.edgeGridLayout.addWidget(distLabel, count, 2)
                firstValueLabel = QLabel("None")
                firstValueLabel.setObjectName(key + 'value1')
                self.edgeGridLayout.addWidget(firstValueLabel, count, 3)
                secondValueLabel = QLabel("None")
                secondValueLabel.setObjectName(key + 'value2')
                self.edgeGridLayout.addWidget(secondValueLabel, count, 4)
                count += 1

    def checkBoxEdited(self, state):
        if state == QtCore.Qt.Checked:
            print("check")
            try:
                self.openRandomDialog(self.sender().objectName())
            except Exception as e:
                print(e)
        else:
            print('unchecked')

    def openRandomDialog(self, name):
        randomDialog = RandomDialog(self.canvas, "Vertex")
        self.setObjectName(name)
        setattr(randomDialog, "update", False)
        randomDialog.exec()
        randomDialog.attrBack.append(name)
        self.attr.append(randomDialog.attrBack)
        print("Self attr: ", self.attr)
        self.notify(randomDialog.attrBack)
        print(self.attr)

    def realTimeEvent(self):
        self.canvas.inRealTimeMode = True
        self.canvas.startRealTime(self.attr)

    def notify(self, mes):
        print(mes)
        dist, value1, value2, name = mes
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


class VertexKeyIgnore(RealTimeDialog):
    ignoredFields = ['hyperedge']


class EdgeKeyIgnore(RealTimeDialog):
    ignoredFields = ['b_delay', 't_delay', 'p_delay', 'key', 'zorder', 'edge_weight']
