from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QCheckBox, QComboBox
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
        self.randomDialog = RandomDialog(self.canvas)
        loadUi('resource/gui/RealTimeDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Real Time Visualization Tool")
        self.checkBoxList = []
        # Vertex tab
        self.vertexGridLayout = self.findChild(QGridLayout, 'vertexGridLayout')
        self.addVertexTitle()
        self.addVertexKey()
        self.selectDistribution = QComboBox()
        self.selectDistribution.addItems([opt for opt in DIST])
        for i in range(len(self.checkBoxList)):
            self.checkBoxList[i].stateChanged.connect(self.checkBoxEdited)

    def addVertexTitle(self):
        count = 0
        for title in TITLE:
            titleLabel = QLabel(title)
            self.vertexGridLayout.addWidget(titleLabel, 0, count)
            count += 1

    def addVertexKey(self):
        count = 1
        for key in self.canvas.g.vs.attributes():
            value = self.canvas.g.vs[0][key]
            keyLabel = QLabel(key)
            if isinstance(value, float) and key not in VertexKeyIgnore.ignoredFields:
                self.vertexGridLayout.addWidget(keyLabel, count, 0)
                checkBox = QCheckBox(self)
                self.checkBoxList.append(checkBox)
                self.vertexGridLayout.addWidget(checkBox, count, 1)
                distLabel = QLabel("None")
                self.vertexGridLayout.addWidget(distLabel, count, 2)
                firstValueLabel = QLabel("None")
                self.vertexGridLayout.addWidget(firstValueLabel, count, 3)
                secondValueLabel = QLabel("None")
                self.vertexGridLayout.addWidget(secondValueLabel, count, 4)

                count += 1

    # def addDistSelectOptions(self, column):

    # self.selectDistribution.currentIndexChanged.connect(self.changeDist)

    def checkBoxEdited(self, state):
        if state == QtCore.Qt.Checked:
            print("check")
            try:
                self.openRandomDialog()
            except Exception as e:
                print(e)
        else:
            print('unchecked')

    def openRandomDialog(self):
        self.randomDialog.exec()


class VertexKeyIgnore(RealTimeDialog):
    ignoredFields = ['hyperedge']
