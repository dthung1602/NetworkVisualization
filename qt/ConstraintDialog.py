from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton
from PyQt5.uic import loadUi

from canvas import Canvas
from .RandomDialog import RandomDialog
from .RenameDialog import RenameDialog
from .utils import clearLayout


class ConstraintDialog(QDialog):
    attrEdge = {"total delay", "link speed raw"}
    attrNode = {"latitude", "longitude"}

    def __init__(self, canvas: Canvas):
        super().__init__()
        self.labelStyleSheet = "font-size: 15px; color: rgb(180,180,180); background-color: transparent;"
        self.buttonStyleSheet = ("QPushButton{"
                                 "color: rgb(200, 200, 200);"
                                 "border-style: 2px solid rgb(200, 200, 200);"
                                 "border-radius: 7px;"
                                 "background-color: #383838; padding: 10px"
                                 "}"
                                 "QPushButton:hover{"
                                 " background-color: #303030;"
                                 "}"
                                 )
        self.canvas = canvas
        self.g = canvas.g
        loadUi('resource/gui/ConstraintDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Checking constraints")
        self.label = self.findChild(QLabel, 'label')
        self.grid = self.findChild(QGridLayout, 'gridLayout')
        self.grid.setAlignment(Qt.AlignTop)
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
        self.notify(edgeMissing, vertexMissing)
        return len(edgeMissing) == 0 and len(vertexMissing) == 0

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
        clearLayout(self.grid)
        self.label.setText(
            'Choose "Rename" if the attribute already exists with another name \n '
            'Choose "Random" to generate data for a missing attribute')
        self.label.setAlignment(Qt.AlignCenter)
        count = 1
        if len(edgeMissing) > 0:
            missLabel = QLabel("Missing attribute of edge:")
            missLabel.setStyleSheet(self.labelStyleSheet)
            self.grid.addWidget(missLabel, 0, 0, 1, 3)
            missLabel.setAlignment(Qt.AlignCenter)
            for i in edgeMissing:
                label = QLabel(i)
                label.setStyleSheet(self.labelStyleSheet)
                label.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(label, count, 0)
                buttonRename = QPushButton('Rename', self)
                buttonRename.setStyleSheet(self.buttonStyleSheet)
                buttonRename.setToolTip('This is rename dialog')
                self.grid.addWidget(buttonRename, count, 1)
                setattr(buttonRename, "type", "EDGE")
                buttonRename.clicked.connect(self.openRenameDialog(i))
                # ========
                buttonRandom = QPushButton('Random', self)
                buttonRandom.setToolTip('This is random dialog')
                buttonRandom.setStyleSheet(self.buttonStyleSheet)
                self.grid.addWidget(buttonRandom, count, 2)
                buttonRandom.clicked.connect(self.openRandomDialog)
                buttonRandom.setObjectName(i)
                setattr(buttonRandom, 'type', 'EDGE')
                count = count + 1
        count = 1
        if len(vertexMissing) > 0:
            missLabel = QLabel("Missing attribute of vertex:")
            missLabel.setStyleSheet(self.labelStyleSheet)
            missLabel.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(missLabel, 0, 3, 1, 3)
            for i in vertexMissing:
                label = QLabel(i)
                label.setStyleSheet(self.labelStyleSheet)
                label.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(label, count, 3)
                buttonRename = QPushButton('Rename', self)
                buttonRename.setStyleSheet(self.buttonStyleSheet)
                buttonRename.setToolTip('This is rename dialog')
                self.grid.addWidget(buttonRename, count, 4)
                setattr(buttonRename, "type", "VERTEX")
                buttonRename.clicked.connect(self.openRenameDialog(i))
                # ========
                buttonRandom = QPushButton('Random', self)
                buttonRandom.setToolTip('This is random dialog')
                buttonRandom.setStyleSheet(self.buttonStyleSheet)
                self.grid.addWidget(buttonRandom, count, 5)
                buttonRandom.clicked.connect(self.openRandomDialog)
                buttonRandom.setObjectName(i)
                setattr(buttonRandom, 'type', 'VERTEX')
                count = count + 1
        if len(vertexMissing) == 0 and len(edgeMissing) == 0:
            missLabel = QLabel("None attribute missing")
            missLabel.setStyleSheet(self.labelStyleSheet)
            self.grid.addWidget(missLabel, 0, 0)
            missLabel.setAlignment(Qt.AlignCenter)

    def openRandomDialog(self):
        randomDialog = RandomDialog(self.canvas, getattr(self.sender(), "type"))
        self.setObjectName(self.sender().objectName())
        randomDialog.exec()

    def openRenameDialog(self, label):
        def func():
            renameDialog = RenameDialog(self.canvas, label)
            renameDialog.exec()
            self.check()

        return func
