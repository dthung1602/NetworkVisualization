from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QLabel
from PyQt5.uic import loadUi

from canvas import Canvas


class RenameDialog(QDialog):
    def __init__(self, canvas: Canvas, newAttributeName):
        super().__init__()
        self.newAttributeName = newAttributeName
        self.canvas = canvas
        loadUi('resource/gui/RenameDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Rename an Attribute")
        self.attribute = self.findChild(QComboBox, 'comboBox')
        self.renameBtn = self.findChild(QPushButton, 'pushButton')
        self.label = self.findChild(QLabel, 'label')
        self.label.setText('Choose an attribute to be renamed as "' + self.newAttributeName + '" ')
        self.type = getattr(self.sender(), "type")
        self.addSelectOptions()

    def addSelectOptions(self):
        if self.type == "EDGE":
            self.attribute.addItems(self.canvas.g.es.attributes())
            self.renameBtn.clicked.connect(self.rename)
        else:
            self.attribute.addItems(self.canvas.g.vs.attributes())
            self.renameBtn.clicked.connect(self.rename)

    def rename(self):
        ev = self.canvas.g.es if self.type == 'EDGE' else self.canvas.g.vs
        key = ev.attributes()[self.attribute.currentIndex()]
        ev[self.newAttributeName] = ev[key]
        del ev[key]
        self.label.setText(f'"{key}" has been renamed to "{self.newAttributeName}"')
