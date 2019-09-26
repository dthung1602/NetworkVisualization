from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Filter(QDialog):
    def __init__(self):
        super().__init__()
        print('Filter Dialog')
        loadUi('resource/gui/FilterDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Filter Dialog")
