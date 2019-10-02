from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.uic import loadUi

from Canvas import Canvas


class WeightDialog(QDialog):
    def __init__(self, canvas: Canvas):
        super().__init__()
        print('graph')
        self.canvas = canvas
        loadUi('resource/gui/WeightDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Input Weight")
        self.selectWeight = self.findChild(QComboBox, 'selectWeight')
        self.addSelectOptions()

    def addSelectOptions(self):
        self.selectWeight.addItems(['-- None --'] + self.canvas.g.es.attributes())
        self.selectWeight.currentIndexChanged.connect(self.changeWeight)

    def changeWeight(self, opt):
        if opt != 0:
            self.canvas.shortestPathWeight = self.canvas.g.es.attributes()[opt-1]
        else:
            self.canvas.shortestPathWeight = None