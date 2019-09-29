#!/usr/bin/env python
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from igraph import *

from Canvas import Canvas
from Filter import Filter
from InfoWidget import EdgeInfoWidget, VertexInfoWidget
from Stat import Stat


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('resource/gui/GUI.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black")
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.mainLayout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.canvas = Canvas(self)
        self.filterWindow = Filter(self.canvas)
        self.statWindow = None # Stat(self.canvas)
        self.mainLayout.addWidget(self.canvas)

        self.infoArea = self.findChild(QVBoxLayout, 'infoArea')
        self.mode = Canvas.MODE_EDIT
        self.bindMenuActions()

    def bindMenuActions(self):
        # -------------- Menu ----------------- #
        # Open_button
        openBtn = self.findChild(QAction, 'action_Open')
        openBtn.triggered.connect(self.openFileNameDialog)
        # Save_Image_button
        saveImageBtn = self.findChild(QAction, 'actionSave_Image')
        saveImageBtn.triggered.connect(self.saveImageDialog)
        # Save_button
        saveBtn = self.findChild(QAction, 'action_Save')
        saveBtn.triggered.connect(self.saveFileDialog)
        # Close_button
        closeBtn = self.findChild(QAction, 'action_Close')
        closeBtn.triggered.connect(self.close)
        # New
        newBtn = self.findChild(QAction, 'actionNew')
        newBtn.triggered.connect(self.newGraph)

        # QMenu.View
        # Zoom in
        self.findChild(QAction, 'actionZoom_In').triggered.connect(self.canvas.zoomInEvent)
        # Zoom out
        self.findChild(QAction, 'actionZoom_Out').triggered.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        self.findChild(QAction, 'actionReset_Zoom').triggered.connect(self.canvas.zoomResetEvent)
        # QMenu.Window
        # Minimize_button
        self.findChild(QAction, 'action_Minimize').triggered.connect(self.minimizeWindow)

        # -------------Toolbar---------------- #
        # Zoom in
        zoomInBtn = self.findChild(QToolButton, 'zoom_in_btn')
        zoomInBtn.pressed.connect(self.canvas.zoomInEvent)
        # Zoom out
        zoomOutBtn = self.findChild(QToolButton, 'zoom_out_btn')
        zoomOutBtn.pressed.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        zoomResetBtn = self.findChild(QToolButton, 'zoom_reset_btn')
        zoomResetBtn.pressed.connect(self.canvas.zoomResetEvent)
        # Color picker
        colorPickerBtn = self.findChild(QToolButton, 'color_picker_btn')
        colorPickerBtn.pressed.connect(self.openColorDialog)
        # Add Node
        addNodeBtn = self.findChild(QToolButton, 'add_node_btn')
        addNodeBtn.pressed.connect(self.addNewNode)
        # Delete Vertex
        deleteBtn = self.findChild(QToolButton, 'delete_node_btn')
        deleteBtn.pressed.connect(self.deleteNodeEvent)
        # Delete Line
        deleteLineBtn = self.findChild(QToolButton, 'delete_line_btn')
        deleteLineBtn.pressed.connect(self.deleteLineEvent)

        # Add Line
        addLineBtn = self.findChild(QToolButton, 'add_line_btn')
        addLineBtn.pressed.connect(self.addLineEvent)
        # Generate graph
        graphBtn = self.findChild(QToolButton, 'graph_btn')
        graphBtn.pressed.connect(self.openGraphEvent)
        # --- Mode ---
        # shortest path
        findShortestPathBtn = self.findChild(QToolButton, 'findShortestPathBtn')
        findShortestPathBtn.pressed.connect(self.activateFindShortestPathMode)
        # bottle neck
        findBottleNeck = self.findChild(QToolButton, 'findBottleNeckBtn')
        findBottleNeck.pressed.connect(self.activateFindBottleNeckMode)
        # edit
        editBtn = self.findChild(QToolButton, 'editBtn')
        editBtn.pressed.connect(self.activateEditGraphMode)
        # open Filter window
        filterBtn = self.findChild(QToolButton, 'filter_dialog_btn')
        filterBtn.pressed.connect(self.openFilterDialog)

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            print(color.name())

    def deleteNodeEvent(self):
        self.canvas.deleteNode = True
        self.canvas.addNode = False
        self.canvas.addLine = False
        self.canvas.deleteLine = False

    def deleteLineEvent(self):
        self.canvas.addNode = False
        self.canvas.deleteNode = False
        self.canvas.deleteLine = True
        self.canvas.addLine = False

    def addNewNode(self):
        self.canvas.addNode = True
        self.canvas.deleteNode = False
        self.canvas.addLine = False
        self.canvas.deleteLine = False

    def addLineEvent(self):
        self.canvas.addLine = True
        self.canvas.deleteNode = False
        self.canvas.addNode = False
        self.canvas.deleteLine = False

    def newGraph(self):
        self.canvas.setGraph(Graph())
        self.canvas.update()

    def saveImageDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As Image", "",
            "All Files (*);;JPG Files (*.jpg)"
        )
        if fileName != '':
            img = QPixmap(self.canvas.size())
            painter = QPainter(img)
            self.canvas.paint(painter)
            painter.end()
            img.save(fileName)

    def minimizeWindow(self):
        if self.windowState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
            # Minimize window
            self.setWindowState(Qt.WindowMinimized)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open", "./resource/graph",
            "All Files (*);;Python Files (*.py)", options=options
        )
        if fileName:
            self.canvas.setGraph(fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "",
            "All Files (*);;GraphML Files (*.graphml);;GML Files (*.gml)", options=options
        )

        if fileName:
            if ".graphml" in fileName:
                self.canvas.g.write_graphml(fileName)
            elif ".gml" in fileName:
                self.canvas.g.write_gml(fileName)

    def activateFindShortestPathMode(self):
        self.mode = Canvas.MODE_FIND_SHORTEST_PATH
        self.canvas.setMode(self.mode)

    def activateEditGraphMode(self):
        self.mode = Canvas.MODE_EDIT
        self.canvas.setMode(self.mode)

    def activateFindBottleNeckMode(self):
        self.mode = Canvas.MODE_FIND_BOTTLE_NECK
        self.canvas.setMode(self.mode)

    @staticmethod
    def clearLayout(layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def displayVertex(self, v):
        self.clearLayout(self.infoArea)
        vertexInfo = VertexInfoWidget(v, self.canvas)
        self.infoArea.addWidget(vertexInfo)

    def displayEdge(self, l):
        self.clearLayout(self.infoArea)
        edgeInfo = EdgeInfoWidget(l, self.canvas)
        self.infoArea.addWidget(edgeInfo)

    def openGraphEvent(self):
        print('Load stat dialog')
        self.statWindow.show()

    def openFilterDialog(self):
        print('Load filter dialog')
        self.filterWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
