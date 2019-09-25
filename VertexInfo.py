from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLayout, QLabel, QVBoxLayout
from PyQt5.uic.properties import QtGui, QtCore


class VertexInfo(QWidget):
    def __init__(self, v):
        super().__init__()
        layout = QVBoxLayout(self)
        # print("Vertex info:" + str(v))
        self.dict = v.attributes()
        # print(self.dict)
        topLabel = QLabel("             VERTEX INFO")
        topLabel.setFont(QFont("Times", 9, QFont.Bold))
        topLabel.setStyleSheet(
            "QLabel { padding: 2px; color: white; background-color: #383838;}")
        layout.addWidget(topLabel)
        for key, value in self.dict.items():
            label = QLabel("• " + str(key) + ": " + str(value))
            label.setWordWrap(True)
            label.setFont(QFont("Times", 8))
            label.setStyleSheet(
                "QLabel {  border: 1px solid rgb(150, 150, 150); padding: 2px; color: rgb(200, 200, 200);"
                " background-color: #383838;"
                "border-radius: 5px; }")
            layout.addWidget(label)
        self.setLayout(layout)
        # print("OK")
