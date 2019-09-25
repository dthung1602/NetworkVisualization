#!/usr/bin/env python
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from igraph import *

from Canvas import Canvas
from EdgeInfo import EdgeInfo
from VertexInfo import VertexInfo

LAYOUT_OPTIONS = [
    ['Circle', 'circle'],
    ['Distributed Recursive', 'drl'],
    ['Fruchterman-Reingold', 'fr'],
    ['Kamada-Kawai', 'kk'],
    ['Large Graph', 'large'],
    ['Random', 'random'],
    ['Reingold-Tilford', 'rt'],
    ['Reingold-Tilford Circular', 'rt_circular']
]

CLUSTERING_ALGOS = [
    ['Fast Greedy', 'community_fastgreedy'],
    ['Info Map', 'community_infomap'],
    ['Label Propagation', 'community_label_propagation'],
    ['Multilevel', 'community_multilevel'],
    ['Optimal Modularity', 'community_optimal_modularity'],
    ['Edge Betweenness', 'community_edge_betweenness'],
    ['Spinglass', 'community_spinglass'],
    ['Walktrap', 'community_walktrap']
]


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('resource/gui/GUI.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black")
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.mainLayout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.canvas = Canvas(self)
        self.mainLayout.addWidget(self.canvas)

        self.selectLayout = self.findChild(QComboBox, 'selectLayout')
        self.selectClusteringAlgo = self.findChild(QComboBox, 'selectClusteringAlgo')
        self.infoArea = self.findChild(QVBoxLayout, 'infoArea')

        self.mode = 'edit'

        self.bindMenuActions()
        self.addSelectOptions()

    def addSelectOptions(self):
        self.selectLayout.addItems([opt[0] for opt in LAYOUT_OPTIONS])
        self.selectLayout.currentIndexChanged.connect(self.changeGraphLayout)
        self.selectClusteringAlgo.addItems([opt[0] for opt in CLUSTERING_ALGOS])
        self.selectClusteringAlgo.currentIndexChanged.connect(self.changeClusteringAlgo)

    def changeGraphLayout(self, opt):
        self.canvas.setGraphLayout(LAYOUT_OPTIONS[opt][1])

    def changeClusteringAlgo(self, opt):
        self.canvas.setClusteringAlgo(CLUSTERING_ALGOS[opt][1])

    def bindMenuActions(self):
        # QMenu.File
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
        # QMenu.View
        #deleteVertex

        # Zoom in
        self.findChild(QAction, 'actionZoom_In').triggered.connect(self.canvas.zoomInEvent)
        # Zoom out
        self.findChild(QAction, 'actionZoom_Out').triggered.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        self.findChild(QAction, 'actionReset_Zoom').triggered.connect(self.canvas.zoomResetEvent)
        # QMenu.Window
        # Minimize_button
        self.findChild(QAction, 'action_Minimize').triggered.connect(self.minimizeWindow)

        # Toolbar
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
        deleteBtn.pressed.connect(self.deleteEvent)

        # Mode
        # shortest path
        findShortestPathBtn = self.findChild(QToolButton, 'findShortestPathBtn')
        findShortestPathBtn.pressed.connect(self.activateFindShortestPathMode)
        # bottle neck
        findBottleNeck = self.findChild(QToolButton, 'findBottleNeckBtn')
        findBottleNeck.pressed.connect(self.activateFindBottleNeckMode)
        # edit
        editBtn = self.findChild(QToolButton, 'editBtn')
        editBtn.pressed.connect(self.activateEditGraphMode)

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            print(color.name())

    def deleteEvent(self):
        self.canvas.deleteNode = True
        self.canvas.addNode = False

    def addNewNode(self):
        self.canvas.addNode = True
        self.canvas.deleteNode = False

    def saveImageDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "",
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
            self, "Open", "",
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
        vertexInfo = VertexInfo(v)
        self.infoArea.addWidget(vertexInfo)

    def displayEdge(self, l):
        self.clearLayout(self.infoArea)
        edgeInfo = EdgeInfo(l)
        self.infoArea.addWidget(edgeInfo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
