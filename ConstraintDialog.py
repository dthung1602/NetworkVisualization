from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QLabel
from PyQt5.uic import loadUi

from Canvas import Canvas


class Constraint(QDialog):
    def __init__(self, canvas: Canvas):
        super().__init__()
        print('graph')
        self.canvas = canvas
        loadUi('resource/gui/ConstraintDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Warning")
        self.selectWeight = self.findChild(QLabel, 'label')
