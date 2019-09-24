from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QLayout, QLabel


class VertexInfo(QWidget):
    def __init__(self, vertex):
        super().__init__()
        self.vertex = vertex
        self.b = QLabel("&Style")
        self.b.insertPlainText("You can write text here.\n")
