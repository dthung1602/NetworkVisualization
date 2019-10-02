from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QGridLayout, QPushButton
from PyQt5.uic import loadUi
from Canvas import Canvas
from RandomDialog import RandomDialog
from RenameDialog import RenameDialog


class Constraint(QDialog):
    attrEdge = {"total delay", "link speed raw"}
    attrNode = {"latitude", "longitude"}

    def __init__(self, canvas: Canvas):
        super().__init__()
        self.canvas = canvas
        self.g = canvas.g
        loadUi('resource/gui/ConstraintDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Warning")
        self.label = self.findChild(QLabel, 'label')
        self.grid = self.findChild(QGridLayout, 'gridLayout')
        self.check()
        self.name = ""

    def checkConstrainEdge(self):
        attr = self.g.es.attributes()
        currAttr = [x.lower() for x in attr]
        missingAttr = []
        for i in self.attrEdge:
            if i not in currAttr:
                missingAttr.append(i)
        return missingAttr

    def checkConstrainVertex(self):
        attr = self.g.vs.attributes()
        currAttr = [x.lower() for x in attr]
        missingAttr = []
        for i in self.attrNode:
            if i not in currAttr:
                missingAttr.append(i)
        return missingAttr

    def check(self):
        edgeMissing = self.checkConstrainEdge()
        vertexMissing = self.checkConstrainVertex()
        if len(edgeMissing) == 0 and len(vertexMissing) == 0:
            return True
        self.notify(edgeMissing, vertexMissing)
        return False

    def link(self, missingAttr, linkAttr, type):
        if type.upper() == "EDGE":
            for i in self.g.es:
                i[linkAttr] = i.attributes()[missingAttr]
                i[missingAttr] = None
        elif type.upper() == "VERTEX":
            for i in self.g.vs:
                i[linkAttr] = i.attributes()[missingAttr]
                i[missingAttr] = None

    def notify(self, edgeMissing, vertexMissing):
        self.label.setText("Warning")
        count = 1
        if len(edgeMissing) > 0:
            self.grid.addWidget(QLabel("Missing attribute of edge"), 0, 0)
            for i in edgeMissing:
                label = QLabel(i)
                self.grid.addWidget(label, count, 0)
                buttonRandom = QPushButton('Rename', self)
                buttonRandom.setToolTip('This is rename dialog')
                self.grid.addWidget(buttonRandom, count, 1)
                buttonRandom.clicked.connect(self.openRenameDialog(i))
                buttonRandom = QPushButton('Random', self)
                buttonRandom.setToolTip('This is random dialog')
                self.grid.addWidget(buttonRandom, count, 2)
                buttonRandom.clicked.connect(self.openRandomDialog)
                buttonRandom.setObjectName(i)
                setattr(buttonRandom, 'type', 'EDGE')
                count = count + 1
        count = 1
        if len(vertexMissing) > 0:
            self.grid.addWidget(QLabel("Missing attribute of vertex"), 0, 3)
            for i in vertexMissing:
                label = QLabel(i)
                self.grid.addWidget(label, count, 3)
                count = count + 1

    def openRandomDialog(self):
        randomDialog = RandomDialog(self.canvas, getattr(self.sender(), "type"))
        self.setObjectName(self.sender().objectName())
        randomDialog.exec()

    def openRenameDialog(self, label):
        def func():
            renameDialog = RenameDialog(self.canvas, label)
            renameDialog.exec()

        return func
