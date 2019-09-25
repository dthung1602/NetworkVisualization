from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLayout, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout
from PyQt5.uic.properties import QtGui, QtCore


class BuddyLabel(QLabel):
    def __init__(self, buddy, parent=None):
        super(BuddyLabel, self).__init__(parent)
        self.buddy = buddy

    # When it's clicked, hide itself and show its buddy
    def mousePressEvent(self, event):
        self.hide()
        self.buddy.show()
        self.buddy.setFocus()  # Set focus on buddy so user doesn't have to click again


class VertexInfo(QWidget):
    def __init__(self, v, canvas):
        super().__init__()
        self.v = v
        self.canvas = canvas
        print("Vertex info:" + str(v))
        self.dict = v.attributes()

        print(self.dict)
        layout = QGridLayout(self)
        topLabelStyleSheet = (
            "font-size: 15px; font-weight: Bold; QLabel; "
            "padding: 2px; color: rgb(220,220,220); background-color: #383838; border-radius: 15px")

        self.topLabel = QLabel('VERTEX INFO')
        self.topLabel.setAlignment(Qt.AlignCenter)
        self.topLabel.setStyleSheet(topLabelStyleSheet)
        layout.addWidget(self.topLabel, 0, 0, 1, 2)

        # layout.addWidget(self.myEdit, 0, 0, 1, 2)

        count = 2
        self.valueLabelItems = []
        self.valueLabelEditItems = []
        for x, y in self.dict.items():
            keyLabel = QLabel(str(x) + ":")
            keyLabel.setWordWrap(True)
            keyLabel.setStyleSheet("QLabel {  font-weight: Bold; font-size: 12px;"
                                   "color: rgb(220,220,220);}")
            layout.addWidget(keyLabel, count, 0)

            valueLabelStyleSheet = ("QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                    "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                    "border-radius: 5px; }")
            valueLabelEdit = QLineEdit()
            valueLabel = BuddyLabel(valueLabelEdit)
            self.valueLabelItems.append(valueLabel)
            self.valueLabelEditItems.append(valueLabelEdit)
            valueLabelEdit.hide()  # Hide line edit
            valueLabelEdit.setStyleSheet(valueLabelStyleSheet)
            valueLabel.setText(str(y))
            valueLabel.setWordWrap(True)
            valueLabel.setStyleSheet(valueLabelStyleSheet)
            hLayout = QHBoxLayout()
            hLayout.addWidget(valueLabelEdit)
            hLayout.addWidget(valueLabel)
            layout.addWidget(valueLabel, count, 1)
            layout.addWidget(valueLabelEdit, count, 1)
            count = count + 1
        self.setLayout(layout)
        print("OK")

        # for i in range(len(self.valueLabelEditItems)):
        #     self.valueLabelEditItems[i].editingFinished.connect(self.textEdited(self.valueLabelItems[i],
        #                                                                         self.valueLabelEditItems[i]))
        # self.valueLabelEditItems[8].editingFinished.connect(self.textEdited(self.valueLabelItems[8],
        # self.valueLabelEditItems[8]))

        # self.valueLabelEditItems[8].editingFinished.connect(self.canvas.update())
        # self.valueLabelEditItems[8].editingFinished.connect(self.test(self.valueLabelEditItems[8]))
        # print(self.valueLabelItems[8].text())

        # print(self.v['y'])

    @staticmethod
    def textEdited(label, edit):
        def func():
            if edit.text():
                label.setText(str(edit.text()))
                edit.hide()
                label.show()
            else:  # If the input is left empty, revert back to the label showing
                edit.hide()
                label.show()

        return func
