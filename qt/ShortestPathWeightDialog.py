from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.uic import loadUi

from canvas import Canvas, ShortestPathMode


class ShortestPathWeightDialog(QDialog):
    def __init__(self, canvas: Canvas, shortestPathMode: ShortestPathMode):
        super().__init__()
        self.canvas = canvas
        self.shortestPathMode = shortestPathMode

        loadUi('resource/gui/ShortestPathWeightDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Input Weight")
        self.selectWeight = self.findChild(QComboBox, 'selectWeight')
        self.addSelectOptions()

    def addSelectOptions(self):
        self.selectWeight.addItems(['-- None --'] + self.canvas.g.es.attributes())
        self.selectWeight.currentIndexChanged.connect(self.changeWeight)

    def changeWeight(self, opt):
        self.shortestPathMode.weight = None if opt == 0 else self.canvas.g.es.attributes()[opt - 1]
