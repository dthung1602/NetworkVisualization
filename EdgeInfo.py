import igraph as ig
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QGroupBox


class EdgeInfo(QWidget):
    def __init__(self, l):
        super().__init__()
        print("Edge info:" + str(l))
        self.dict = l.attributes()

        print(self.dict)
        layout = QGridLayout(self)
        topLabel = QLabel("EDGE INFO")
        topLabel.setAlignment(Qt.AlignCenter)
        topLabel.setFont(QFont("Times", 9, QFont.Bold))
        topLabel.setStyleSheet(
            "QLabel { padding: 2px; color: white; background-color: #383838;}")
        layout.addWidget(topLabel, 0, 0, 1, 2)
        infoStyleSheet = "QLabel {  font-size: 11px; border: 1px solid rgb(150, 150, 150); " \
                     "padding: 2px; color: white; background-color: #383838;""border-radius: 5px; }"

        count = 2
        for x, y in self.dict.items():
            keyLabel = QLabel(str(x))
            keyLabel.setWordWrap(True)
            keyLabel.setStyleSheet(infoStyleSheet)
            layout.addWidget(keyLabel, count, 0)
            valueLabel = QLabel(str(y))
            valueLabel.setWordWrap(True)
            valueLabel.setStyleSheet(infoStyleSheet)
            layout.addWidget(valueLabel, count, 1)
            count = count + 1
        self.setLayout(layout)

    def printInfo(self):
        for attr in self.dictAttr:
            print("Key = ", attr, " Value = ", self.dictAttr[attr])
