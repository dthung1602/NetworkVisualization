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
        self.dict = self.v.attributes()
        print(self.dict)

        # Title layout
        layout = QGridLayout(self)
        topLabelStyleSheet = (
            "font-size: 15px; font-weight: Bold; QLabel; "
            "padding: 2px; color: rgb(220,220,220); background-color: #383838; border-radius: 15px")

        self.topLabel = QLabel('VERTEX INFO')
        self.topLabel.setAlignment(Qt.AlignCenter)
        self.topLabel.setStyleSheet(topLabelStyleSheet)
        layout.addWidget(self.topLabel, 0, 0, 1, 2)

        # Info layout
        count = 2
        self.valueLabelItems = []
        self.valueLabelEditItems = []
        for x, y in self.dict.items():
            keyLabel = QLabel(str(x) + ":")
            keyLabel.setWordWrap(True)
            keyLabel.setStyleSheet("QLabel {  background-color: #414141; font-weight: Bold; font-size: 11px;"
                                   "color: rgb(220,220,220); border-radius: 5px; padding-left: 3px; }")
            layout.addWidget(keyLabel, count, 0)

            valueLabelStyleSheet = ("QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                    "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                    "border-radius: 5px; }"
                                    "QLabel:hover{background-color: #242424; cursor: pointer;}")
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

        # Update info
        for i in range(len(self.valueLabelEditItems)):
            self.valueLabelEditItems[i].editingFinished.connect(self.textEdited(self.valueLabelItems[i],
                                                                                self.valueLabelEditItems[i]))
            self.valueLabelEditItems[i].editingFinished.connect(self.saveInfo)

    @staticmethod
    def textEdited(label, edit):
        def func():
            if edit.text():
                label.setText(str(edit.text()))
                edit.hide()
                label.show()
                print('changed')
            else:
                # If the input is left empty, revert back to the label showing
                print('no changed')
                edit.hide()
                label.show()

        return func

    def saveInfo(self):
        for i, count in zip(self.v.attributes(), range(len(self.valueLabelItems))):
            # print(i)
            # print(self.valueLabelItems[count].text())
            if isinstance(self.v[i], str):
                # print('>> Receive string ')
                self.v[i] = self.valueLabelItems[count].text()
            elif isinstance(self.v[i], float):
                # print('>> Receive float ')
                self.v[i] = float(self.valueLabelItems[count].text())

        self.canvas.update()
