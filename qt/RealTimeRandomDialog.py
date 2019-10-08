import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.uic import loadUi

from canvas import Canvas
from .utils import BuddyLabel, clearLayout, textEdited

DIST = [
    'Normal distribution',
    'Uniform distribution'
]


class RealTimeRandomDialog(QDialog):
    def __init__(self, canvas: Canvas, type):
        super().__init__()
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
        self.generateBtn = self.findChild(QPushButton, 'generate_btn')
        self.notiLabel = self.findChild(QLabel, 'notiLabel')
        self.notiLabel.setWordWrap(True)
        self.addDistSelectOptions()
        self.labelStyleSheet = ("color: rgb(180,180,180);"
                                "font-size: 15px;"
                                "background-color: transparent;")
        self.buttonStyleSheet = ("QPushButton{"
                                 "color: rgb(200, 200, 200);"
                                 "border-style: 2px solid rgb(200, 200, 200);"
                                 "border-radius: 7px;"
                                 "background-color: #383838;"
                                 "}"
                                 "QPushButton:hover{"
                                 " background-color: #303030;"
                                 "}"
                                 )

        self.valueLabelStyleSheet = ("QLabel { font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                     "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                     "border-radius: 5px; }"
                                     "QLabel:hover {background-color: #242424;}"
                                     "QLineEdit {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                     "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                     "border-radius: 5px; }"
                                     "QLineEdit:hover{background-color: #242424;}")

        self.meanEdit = QLineEdit()
        self.mean = BuddyLabel(self.meanEdit)

        self.standardDeviationEdit = QLineEdit()
        self.standardDeviation = BuddyLabel(self.standardDeviationEdit)

        self.minEdit = QLineEdit()
        self.min = BuddyLabel(self.minEdit)

        self.intervalEdit = QLineEdit()
        self.interval = BuddyLabel(self.intervalEdit)

        self.valueLabelStyleSheet = ("QLabel { font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                     "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                     "border-radius: 5px; }"
                                     "QLabel:hover{background-color: #242424;}"
                                     "QLineEdit {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                     "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                     "border-radius: 5px; }"
                                     "QLineEdit:hover{background-color: #242424;}")
        self.attrBack = []

        self.randomArr = []
        self.update = True

    def changeDist(self, opt):
        [
            self.default,
            self.normalDistribution,
            self.uniformDistribution,
        ][opt]()

    def addDistSelectOptions(self):
        self.selectDistribution.addItems(['-- None --'])
        self.selectDistribution.addItems([opt for opt in DIST])
        self.selectDistribution.currentIndexChanged.connect(self.changeDist)

    def default(self):
        clearLayout(self.randomLayout)

    def normalDistribution(self):
        clearLayout(self.randomLayout)

        stdevLabel = QLabel('Standard Deviation: ')
        stdevLabel.setStyleSheet(self.labelStyleSheet)
        self.randomLayout.addWidget(stdevLabel)
        self.standardDeviationEdit.setStyleSheet(self.valueLabelStyleSheet)
        self.standardDeviation.setStyleSheet(self.valueLabelStyleSheet)
        self.randomLayout.addWidget(self.standardDeviation)
        self.randomLayout.addWidget(self.standardDeviationEdit)

        self.standardDeviationEdit.editingFinished.connect(
            textEdited(self.standardDeviation, self.standardDeviationEdit))
        self.generateBtn.pressed.connect(self.generateNormalDistribution)

    def uniformDistribution(self):

        try:
            clearLayout(self.randomLayout)

            maxLabel = QLabel('Interval: ')
            maxLabel.setStyleSheet(self.labelStyleSheet)
            self.interval.setStyleSheet(self.valueLabelStyleSheet)
            self.intervalEdit.setStyleSheet(self.valueLabelStyleSheet)
            self.randomLayout.addWidget(maxLabel)
            self.randomLayout.addWidget(self.interval)
            self.randomLayout.addWidget(self.intervalEdit)

            self.intervalEdit.editingFinished.connect(textEdited(self.interval, self.intervalEdit))
            self.generateBtn.pressed.connect(self.generateUniformDistribution)
        except Exception as e:
            print(e.__traceback__.tb_lineno, " ", e)

    def generateNormalDistribution(self):
        stdDeviation = float(self.standardDeviationEdit.text())
        print(stdDeviation)
        self.notiLabel.setText(
            "Generated Normal Distribution with \n Standard Deviation = " + str(stdDeviation))
        self.attrBack.append("Normal Distribution")
        self.attrBack.append(stdDeviation)

    def generateUniformDistribution(self):

        try:
            val = float(self.intervalEdit.text())
            print("Interval = ", val)
            self.notiLabel.setText("Generated Uniform Distribution with \n interval = " + str(val))
            self.attrBack.append("Uniform Distribution")
            self.attrBack.append(val)
        except Exception as e:
            print(e.__traceback__.tb_lineno, " ", e)

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
