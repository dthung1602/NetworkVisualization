from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout, QLabel, QLineEdit
from PyQt5.uic import loadUi

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
    def __init__(self, canvas: Canvas):
        super().__init__()
        print('Random Dialog')
        self.canvas = canvas
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

    def changeDist(self, opt):
        [
            self.normalDistribution,
            self.uniformDistribution,
        ][opt]()

    def normalDistribution(self):
        self.clearLayout(self.randomLayout)
        print("normal")
        meanLabel = QLabel('Mean: ')
        self.randomLayout.addWidget(meanLabel)
        self.randomLayout.addWidget(self.mean)
        self.randomLayout.addWidget(self.meanEdit)

        stdevLabel = QLabel('Standard Deviation: ')
        self.randomLayout.addWidget(stdevLabel)
        self.randomLayout.addWidget(self.standardDeviation)
        self.randomLayout.addWidget(self.standardDeviationEdit)



    def uniformDistribution(self):
        print("uniform")
        self.clearLayout(self.randomLayout)
        minLabel = QLabel('Min: ')
        self.randomLayout.addWidget(minLabel)
        self.randomLayout.addWidget(self.min)
        self.randomLayout.addWidget(self.minEdit)

        maxLabel = QLabel('Max: ')
        self.randomLayout.addWidget(maxLabel)
        self.randomLayout.addWidget(self.max)
        self.randomLayout.addWidget(self.maxEdit)

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
