from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QLabel
from PyQt5.uic import loadUi

from Canvas import Canvas


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
        self.type = getattr(self.sender(),"type")
        self.addSelectOptions()

    def addSelectOptions(self):
        if self.type == "EDGE":
            self.attribute.addItems(self.canvas.g.es.attributes())
            self.renameBtn.clicked.connect(self.rename)
        else:
            self.attribute.addItems(self.canvas.g.vs.attributes())
            self.renameBtn.clicked.connect(self.rename)

    def rename(self):
        if self.type=="EDGE":
            opt = int(self.attribute.currentIndex())
            key = self.canvas.g.es.attributes()[opt]
            self.canvas.g.es[self.newAttributeName] = self.canvas.g.es[key]
            del self.canvas.g.es[key]
            self.label.setText('"' + key + '"' + ' has been renamed to ' + '"' + self.newAttributeName + '"')
        if self.type=="VERTEX":
            opt = int(self.attribute.currentIndex())
            key = self.canvas.g.vs.attributes()[opt]
            self.canvas.g.vs[self.newAttributeName] = self.canvas.g.vs[key]
            del self.canvas.g.vs[key]
            self.label.setText('"' + key + '"' + ' has been renamed to ' + '"' + self.newAttributeName + '"')
