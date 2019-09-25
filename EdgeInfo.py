from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout


class EdgeInfo(QWidget):
    def __init__(self, l):
        super().__init__()
        self.dict = l.attributes()
        styleSheet = "QLabel {  border: 1px solid rgb(150, 150, 150); padding: 2px; color: white; background-color: #383838;""border-radius: 5px; }"
        layout = QGridLayout(self)
        topLabel = QLabel("Edge INFO")
        topLabel.setFont(QFont("Times", 9, QFont.Bold))
        topLabel.setStyleSheet(
            "QLabel { padding: 2px; color: white; background-color: #383838;}")
        layout.addWidget(topLabel, 1, 1)
        count = 2
        for x, y in self.dict.items():
            keyLabel = QLabel(str(x))
            keyLabel.setWordWrap(True)
            keyLabel.setFont(QFont("Times", 8))
            keyLabel.setStyleSheet(styleSheet)
            layout.addWidget(keyLabel, count, 0)
            valueLabel = QLabel(str(y))
            valueLabel.setWordWrap(True)
            valueLabel.setFont(QFont("Times", 8))
            valueLabel.setStyleSheet(styleSheet)
            layout.addWidget(valueLabel, count, 1)
            count = count + 1
        self.setLayout(layout)

    def printInfo(self):
        pass
        # for attr in self.dictAttr:
        #     print("Key = ", attr, " Value = ", self.dictAttr[attr])
