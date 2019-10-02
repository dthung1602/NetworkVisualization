from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QPushButton, QLabel
from PyQt5.uic import loadUi

from Canvas import Canvas


class RenameDialog(QDialog):
    def __init__(self, canvas: Canvas, newAttributeName):
        super().__init__()
        print('Rename')
        self.newAttributeName = newAttributeName
        print(self.newAttributeName)
        self.canvas = canvas
        loadUi('resource/gui/RenameDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Rename an Attribute")
        self.attribute = self.findChild(QComboBox, 'comboBox')
        self.renameBtn = self.findChild(QPushButton, 'pushButton')
        self.label = self.findChild(QLabel, 'label')
        self.addSelectOptions()

    def addSelectOptions(self):
        self.attribute.addItems(self.canvas.g.es.attributes())
        #self.renameBtn.clicked.connect(self.rename)
        self.attribute.currentIndexChanged.connect(self.rename)

    def rename(self):
        opt = int(self.attribute.currentIndex())
        print("RENAME")
        key = self.canvas.g.es.attributes()[opt]
        print(key)
        self.canvas.g.es[self.newAttributeName] = self.canvas.g.es[key]
        del self.canvas.g.es[key]
        self.label.setText(key + 'has been renamed to ' + self.newAttributeName)
