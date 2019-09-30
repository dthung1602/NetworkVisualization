from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QHBoxLayout


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


class InfoWidget(QWidget):
    title = ''
    ignoredFields = []

    def __init__(self, value, canvas):
        super().__init__()
        self.value = value
        self.canvas = canvas

        self.dict = value.attributes()
        for f in self.ignoredFields:
            del self.dict[f]

        # Title layout
        layout = QGridLayout(self)
        topLabelStyleSheet = (
            "font-size: 15px; font-weight: Bold; QLabel; "
            "padding: 2px; color: rgb(220,220,220); background-color: #383838; border-radius: 15px")

        self.topLabel = QLabel(self.title)
        self.topLabel.setAlignment(Qt.AlignCenter)
        self.topLabel.setStyleSheet(topLabelStyleSheet)
        layout.addWidget(self.topLabel, 0, 0, 1, 2)

        # Info layout
        count = 2
        self.valueLabelItems = []
        self.valueLabelEditItems = []
        for label, text in self.dict.items():
            text = str(text)
            keyLabel = QLabel(str(label) + ":")
            keyLabel.setWordWrap(True)
            keyLabel.setStyleSheet("QLabel {  background-color: #414141; font-weight: Bold; font-size: 11px;"
                                   "color: rgb(220,220,220); border-radius: 5px; padding-left: 3px; }")
            layout.addWidget(keyLabel, count, 0)

            valueLabelStyleSheet = ("QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); "
                                    "padding: 2px; color: rgb(220,220,220); background-color: #383838;"
                                    "border-radius: 5px; }"
                                    "QLabel:hover{background-color: #242424;}")
            valueLabelEdit = QLineEdit()
            valueLabel = BuddyLabel(valueLabelEdit)
            self.valueLabelItems.append(valueLabel)
            self.valueLabelEditItems.append(valueLabelEdit)
            valueLabelEdit.setStyleSheet(valueLabelStyleSheet)
            valueLabel.setText(text)
            valueLabelEdit.setText(text)
            valueLabel.setWordWrap(True)
            valueLabel.setStyleSheet(valueLabelStyleSheet)
            hLayout = QHBoxLayout()
            hLayout.addWidget(valueLabelEdit)
            hLayout.addWidget(valueLabel)
            layout.addWidget(valueLabel, count, 1)
            layout.addWidget(valueLabelEdit, count, 1)
            count = count + 1
        self.setLayout(layout)

        # Update info
        for i in range(len(self.valueLabelEditItems)):
            func = self.textEdited(self.valueLabelItems[i], self.valueLabelEditItems[i])
            self.valueLabelEditItems[i].editingFinished.connect(func)
            self.valueLabelEditItems[i].editingFinished.connect(self.saveInfo)

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

    def saveInfo(self):
        for i, count in zip(self.value.attributes(), range(len(self.valueLabelItems))):
            newValue = self.valueLabelItems[count].text()
            try:
                newValue = float(newValue)
            except ValueError:
                pass
            self.value[i] = newValue

        self.canvas.update()


class VertexInfoWidget(InfoWidget):
    title = 'VERTEX INFO'
    ignoredFields = ['color', 'pos', 'degree']


class EdgeInfoWidget(InfoWidget):
    title = 'EDGE INFO'
    ignoredFields = ['line']
