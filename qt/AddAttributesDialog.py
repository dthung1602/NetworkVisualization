from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.uic import loadUi

from canvas import Canvas


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


class AddAttributesDialog(QDialog):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self.canvas = canvas

        loadUi('resource/gui/AddAttributesDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Add Attributes for Vertexes/Edges")

        # ------------Vertex-----------------
        self.layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.button = self.findChild(QPushButton, 'acceptButton')

        self.label = QLabel('Attribute name: ')
        self.label.setStyleSheet("color: rgb(180,180,180); font-size: 15px; background-color: transparent;")
        self.layout.addWidget(self.label)
        valueLabelStyleSheet = ("QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                "border-radius: 5px; }"
                                "QLabel:hover{background-color: #242424;}")

        self.valueEdit = QLineEdit()
        self.valueEdit.setStyleSheet(valueLabelStyleSheet)
        self.value = BuddyLabel(self.valueEdit)

        self.value.setStyleSheet(valueLabelStyleSheet)

        self.layout.addWidget(self.value)
        self.layout.addWidget(self.valueEdit)

        self.button.clicked.connect(self.textEdited(self.value, self.valueEdit))
        self.button.clicked.connect(self.saveVertexInfo)

        # ------------Edge-----------------
        self.layout2 = self.findChild(QVBoxLayout, 'verticalLayout_2')
        self.button2 = self.findChild(QPushButton, 'acceptButton_2')

        self.label2 = QLabel('Attribute name: ')
        self.label2.setStyleSheet("color: rgb(180,180,180); font-size: 15px; background-color: transparent;")
        self.layout2.addWidget(self.label2)

        self.valueEdit2 = QLineEdit()
        self.valueEdit2.setStyleSheet(valueLabelStyleSheet)
        self.value2 = BuddyLabel(self.valueEdit2)

        self.value2.setStyleSheet(valueLabelStyleSheet)

        self.layout2.addWidget(self.value2)
        self.layout2.addWidget(self.valueEdit2)

        self.button2.clicked.connect(self.textEdited(self.value2, self.valueEdit2))
        self.button2.clicked.connect(self.saveEdgeInfo)

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

    def saveVertexInfo(self):
        valueEdited = str(self.valueEdit.text())
        self.canvas.g.vs[valueEdited] = ""
        self.label.setText(valueEdited + " has been successfully added!")

    def saveEdgeInfo(self):
        valueEdited = str(self.valueEdit2.text())
        self.canvas.g.es[valueEdited] = ""
        self.label2.setText(valueEdited + " has been successfully added!")
