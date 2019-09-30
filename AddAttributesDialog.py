from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QTextEdit, QVBoxLayout, QLabel, QLineEdit
from PyQt5.uic import loadUi

from Canvas import Canvas


class BuddyLabel(QLabel):
    def __init__(self, buddy, parent=None):
        super(BuddyLabel, self).__init__(parent)
        self.buddy = buddy
        self.buddy.hide()

    # When it's clicked, hide itself and show its buddy
    def mousePressEvent(self, event):
        self.hide()
        self.buddy.show()
        self.buddy.setFocus()  # Set focus on buddy so user doesn't have to click againe


class WeightDialog(QDialog):
    def __init__(self, canvas: Canvas):
        super().__init__()
        print('graph')
        self.canvas = canvas
        loadUi('resource/gui/WeightDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Add Attributes for Vertexes")
        self.layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.verticalLayout.addWidget(QLabel('Attribute name: '))
        valueLabelStyleSheet = ("QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                "border-radius: 5px; }"
                                "QLabel:hover{background-color: #242424;}")
        self.valueEdit = QLineEdit()
        self.valueEdit.setStyleSheet(valueLabelStyleSheet)
        self.value = BuddyLabel(self.valueEdit)
        self.value.setStyleSheet(valueLabelStyleSheet)
        self.value.editingFinished.connect(self.textEdited())
        self.layout.addWidget(self.value)
        self.layout.addWidget(self.valueEdit)

    def addAttribute(self):
        pass

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
