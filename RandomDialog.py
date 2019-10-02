from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.uic import loadUi
import numpy as np
from Canvas import Canvas

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


class RandomDialog(QDialog):
    def __init__(self, canvas: Canvas, type):
        super().__init__()
        print('Random Dialog')
        self.canvas = canvas
        self.type = type
        self.g = canvas.g
        self.attr = self.sender().objectName()
        loadUi('resource/gui/RandomDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Random data")
        self.distLayout = self.findChild(QVBoxLayout, 'distLayout')
        self.selectDistribution = self.findChild(QComboBox, 'distBox')
        self.randomLayout = self.findChild(QVBoxLayout, 'randomLayout')
        self.addDistSelectOptions()

        self.meanEdit = QLineEdit()
        self.mean = BuddyLabel(self.meanEdit)

        self.standardDeviationEdit = QLineEdit()
        self.standardDeviation = BuddyLabel(self.standardDeviationEdit)

        self.minEdit = QLineEdit()
        self.min = BuddyLabel(self.minEdit)

        self.maxEdit = QLineEdit()
        self.max = BuddyLabel(self.maxEdit)

        self.valueLabelStyleSheet = ("QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                     "padding: 2px; color: rgb(220,220,220); border-radius: 5px;}"
                                     "QLabel:hover{background-color: #242424;}")
        self.attrBack = []

    def changeDist(self, opt):
        [
            self.normalDistribution,
            self.uniformDistribution,
        ][opt]()

    def addDistSelectOptions(self):
        self.selectDistribution.addItems([opt for opt in DIST])
        self.selectDistribution.currentIndexChanged.connect(self.changeDist)

    def normalDistribution(self):
        self.clearLayout(self.randomLayout)
        print("normal")
        meanLabel = QLabel('Mean: ')
        self.mean.setStyleSheet(self.valueLabelStyleSheet)
        self.meanEdit.setStyleSheet(self.valueLabelStyleSheet)
        self.randomLayout.addWidget(meanLabel)
        self.randomLayout.addWidget(self.mean)
        self.randomLayout.addWidget(self.meanEdit)

        stdevLabel = QLabel('Standard Deviation: ')
        self.randomLayout.addWidget(stdevLabel)
        self.standardDeviationEdit.setStyleSheet(self.valueLabelStyleSheet)
        self.standardDeviation.setStyleSheet(self.valueLabelStyleSheet)
        self.randomLayout.addWidget(self.standardDeviation)
        self.randomLayout.addWidget(self.standardDeviationEdit)

        acceptBtn = QPushButton('OK', self)
        self.randomLayout.addWidget(acceptBtn)
        acceptBtn.clicked.connect(self.textEdited(self.mean, self.meanEdit))
        acceptBtn.clicked.connect(self.textEdited(self.standardDeviation, self.standardDeviationEdit))
        acceptBtn.clicked.connect(self.generateNormalDistribution)

    def uniformDistribution(self):
        print("uniform")
        self.clearLayout(self.randomLayout)
        minLabel = QLabel('Min: ')
        self.minEdit.setStyleSheet(self.valueLabelStyleSheet)
        self.min.setStyleSheet(self.valueLabelStyleSheet)
        self.randomLayout.addWidget(minLabel)
        self.randomLayout.addWidget(self.min)
        self.randomLayout.addWidget(self.minEdit)

        maxLabel = QLabel('Max: ')
        self.max.setStyleSheet(self.valueLabelStyleSheet)
        self.maxEdit.setStyleSheet(self.valueLabelStyleSheet)
        self.randomLayout.addWidget(maxLabel)
        self.randomLayout.addWidget(self.max)
        self.randomLayout.addWidget(self.maxEdit)

        acceptBtn = QPushButton('OK', self)
        self.randomLayout.addWidget(acceptBtn)
        acceptBtn.clicked.connect(self.textEdited(self.min, self.minEdit))
        acceptBtn.clicked.connect(self.textEdited(self.max, self.maxEdit))
        acceptBtn.clicked.connect(self.generateUniformDistribution)

    @staticmethod
    def textEdited(label, edit):
        def func():
            if edit.text():
                label.setText(str(edit.text()))
                edit.hide()
                label.show()
            else:
                # If the input is left empty, revert back to the label showing
                edit.hide()
                label.show()

        return func

    @staticmethod
    def clearLayout(layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def generateNormalDistribution(self):

        print("generateNormalDistribution ", self.attr)
        mean = float(self.meanEdit.text())
        stdDeviation = float(self.standardDeviationEdit.text())

        if self.type == 'EDGE':
            size = self.g.ecount()
            randomArr = np.random.normal(mean, stdDeviation, size)
            self.changeEdge(self.attr, randomArr)
        else:
            size = self.g.vcount()
            randomArr = np.random.normal(mean, stdDeviation, size)
            self.changeVertex(self.attr, randomArr)
        self.attrBack.append("Normal Distribution")
        self.attrBack.append(mean)
        self.attrBack.append(stdDeviation)
        print('Generate Norm ')

    def generateUniformDistribution(self):
        min = float(self.minEdit.text())
        max = float(self.maxEdit.text())
        if self.type == 'EDGE':
            size = self.g.ecount()
            randomArr = np.random.uniform(min, max, size)
            self.changeEdge(self.attr, randomArr)
        else:
            size = self.g.vcount()
            randomArr = np.random.uniform(min, max, size)
            self.changeVertex(self.attr, randomArr)
        self.attrBack.append("Uniform Distribution")
        self.attrBack.append(min)
        self.attrBack.append(max)

    def changeEdge(self, attributeName, randomArr):
        count = 0
        for i in self.g.es:
            i[attributeName] = randomArr[count]
            count = count + 1

    def changeVertex(self, attributeName, randomArr):
        count = 0
        for i in self.g.vs:
            i[attributeName] = randomArr[count]
            count = count + 1

    def getAttr(self):
        return self.attrBack
