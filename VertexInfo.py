from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLayout, QLabel, QVBoxLayout, QGridLayout
from PyQt5.uic.properties import QtGui, QtCore


class VertexInfo(QWidget):
    def __init__(self, v):
        super().__init__()
        print("Vertex info:" + str(v))
        self.dict = v.attributes()

        print(self.dict)
        layout = QGridLayout(self)
        topLabel = QLabel("VERTEX INFO")
        topLabel.setAlignment(Qt.AlignCenter)
        topLabel.setFont(QFont("SansSerif", 9, QFont.Bold))
        topLabel.setStyleSheet(
            "QLabel { padding: 2px; color: white; background-color: #383838;}")
        layout.addWidget(topLabel, 0, 0, 1, 2)

        infoStyleSheet = "QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); " \
                         "padding: 2px; color: white; background-color: #383838;" \
                         " border-radius: 5px; }"
        count = 2
        for x, y in self.dict.items():
            keyLabel = QLabel(str(x) + ":")
            keyLabel.setWordWrap(True)
            # keyLabel.setFont(QFont("SansSerif", 8))
            keyLabel.setStyleSheet(infoStyleSheet)
            layout.addWidget(keyLabel, count, 0)
            valueLabel = QLabel(str(y))
            valueLabel.setWordWrap(True)
            # valueLabel.setFont(QFont("SansSerif", 8))
            valueLabel.setStyleSheet(infoStyleSheet)
            layout.addWidget(valueLabel, count, 1)
            count = count + 1
        self.setLayout(layout)
        print("OK")
