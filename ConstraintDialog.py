from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QGridLayout
from PyQt5.uic import loadUi
from Canvas import Canvas


class Constraint(QDialog):
    attrEdge = {"total delay", "link speed raw"}
    attrNode = {"latitude", "longitude"}

    def __init__(self, canvas: Canvas):
        super().__init__()
        print('graph')
        self.g = canvas.g
        loadUi('resource/gui/ConstraintDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Warning")
        self.label = self.findChild(QLabel, 'label')
        self.grid = self.findChild(QGridLayout, 'gridLayout')
        print("Checkhere")
        self.check()

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
        print(edgeMissing)
        print(vertexMissing)
        if (len(edgeMissing) == 0 and len(vertexMissing) == 0):
            return True
        print("Check false")
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
        if (len(edgeMissing) > 0):
            self.grid.addWidget(QLabel("Missing attribute of edge"), 0, 0)
            for i in edgeMissing:
                label = QLabel(i)
                self.grid.addWidget(label, count, 0)
                count = count + 1
        count = 1
        if (len(vertexMissing) > 0):
            self.grid.addWidget(QLabel("Missing attribute of vertex"), 0, 1)
            for i in vertexMissing:
                label = QLabel(i)
                self.grid.addWidget(label, count, 1)
                count = count + 1
        print("Missing requirement attributes. Please choose input method")
