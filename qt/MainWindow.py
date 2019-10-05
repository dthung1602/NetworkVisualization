import igraph
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import *

from canvas import Canvas
from canvas.utils import DARK_MODE, LIGHT_MODE, GEO_MODE
from .AddAttributesDialog import AddAttributesDialog
from .ConstraintDialog import ConstraintDialog
from .FilterDialog import FilterDialog
from .InfoWidget import EdgeInfoWidget, VertexInfoWidget
from .RealTimeDialog import *
from .StatDialog import StatDialog
from .WeightDialog import WeightDialog
from .utils import clearLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('resource/gui/GUI.ui', self)

        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black")
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.canvas = Canvas(self)
        self.findChild(QVBoxLayout, 'verticalLayout').addWidget(self.canvas)

        self.filterDialog = FilterDialog(self.canvas)  # TODO qwidget vs qdialog
        self.statDialog = StatDialog(self.canvas)
        self.weightDialog = WeightDialog(self.canvas)
        self.constraintDialog = ConstraintDialog(self.canvas)
        self.addAttributesDialog = AddAttributesDialog(self.canvas)
        self.realTimeDialog = RealTimeDialog(self.canvas)

        self.infoArea = self.findChild(QVBoxLayout, 'infoArea')
        self.canvas.setViewMode(DARK_MODE)
        self.bindMenuActions()

    def bindMenuActions(self):
        # ------------- Menu ---------------- #
        # File
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

        # View
        # Zoom in
        self.findChild(QAction, 'actionZoom_In').triggered.connect(self.canvas.zoomInEvent)
        # Zoom out
        self.findChild(QAction, 'actionZoom_Out').triggered.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        self.findChild(QAction, 'actionReset_Zoom').triggered.connect(self.canvas.zoomResetEvent)
        # View mode
        self.findChild(QAction, 'actionGeographical_Mode').triggered.connect(self.changeViewModeTo(GEO_MODE))
        self.findChild(QAction, 'actionDark_Mode').triggered.connect(self.changeViewModeTo(DARK_MODE))
        self.findChild(QAction, 'actionLight_Mode').triggered.connect(self.changeViewModeTo(LIGHT_MODE))

        # Window
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
        # Add vertex
        addVertexBtn = self.findChild(QToolButton, 'add_node_btn')
        addVertexBtn.pressed.connect(self.addVertex)
        # Delete Vertex
        deleteBtn = self.findChild(QToolButton, 'delete_node_btn')
        deleteBtn.pressed.connect(self.deleteVertex)
        # Add Line
        addLineBtn = self.findChild(QToolButton, 'add_line_btn')
        addLineBtn.pressed.connect(self.addLine)
        # Delete Line
        deleteLineBtn = self.findChild(QToolButton, 'delete_line_btn')
        deleteLineBtn.pressed.connect(self.deleteLine)

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
        # Generate stat
        graphBtn = self.findChild(QToolButton, 'graph_btn')
        graphBtn.pressed.connect(self.openStatDialog)
        # open Filter window
        filterBtn = self.findChild(QToolButton, 'filter_dialog_btn')
        filterBtn.pressed.connect(self.openFilterDialog)
        # Open Constraint Dialog
        constraintBtn = self.findChild(QToolButton, 'constraint_btn')
        constraintBtn.pressed.connect(self.openConstraintDialog)
        # Add Attributes Dialog
        addAttributeBtn = self.findChild(QToolButton, 'add_attribute_btn')
        addAttributeBtn.pressed.connect(self.openAddAttributesDialog)
        # Real Time Dialog
        realTimeBtn = self.findChild(QToolButton, 'real_time_btn')
        realTimeBtn.pressed.connect(self.openRealTimeDialog)

    def openAddAttributesDialog(self):
        self.addAttributesDialog.exec()

    def openConstraintDialog(self):
        self.constraintDialog.exec()
        self.constraintDialog.check()

    def changeViewModeTo(self, viewMode):
        def func():
            self.canvas.setViewMode(viewMode)
            self.canvas.update()

        return func

    def deleteVertex(self):
        self.canvas.deleteNode = True
        self.canvas.addNode = False
        self.canvas.addLine = False
        self.canvas.deleteLine = False

    def deleteLine(self):
        self.canvas.addNode = False
        self.canvas.deleteNode = False
        self.canvas.deleteLine = True
        self.canvas.addLine = False

    def addVertex(self):
        self.canvas.addNode = True
        self.canvas.deleteNode = False
        self.canvas.addLine = False
        self.canvas.deleteLine = False

    def addLine(self):
        self.canvas.addLine = True
        self.canvas.deleteNode = False
        self.canvas.addNode = False
        self.canvas.deleteLine = False

    def newGraph(self):
        g = igraph.read('resource/graph/__empty__.graphml')
        self.canvas.setGraph(g)
        self.canvas.center = QPointF(530, 1130)
        self.canvas.zoom = 0.25
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
        self.weightDialog.exec()
        self.canvas.setMode(Canvas.MODE_FIND_SHORTEST_PATH)

    def activateEditGraphMode(self):
        self.canvas.setMode(Canvas.MODE_EDIT)

    def activateFindBottleNeckMode(self):
        self.canvas.setMode(Canvas.MODE_FIND_BOTTLE_NECK)

    def displayVertex(self, v):
        clearLayout(self.infoArea)
        vertexInfo = VertexInfoWidget(v, self.canvas)
        self.infoArea.addWidget(vertexInfo)

    def displayEdge(self, l):
        clearLayout(self.infoArea)
        edgeInfo = EdgeInfoWidget(l, self.canvas)
        self.infoArea.addWidget(edgeInfo)

    def openStatDialog(self):
        self.statDialog.show()

    def openFilterDialog(self):
        self.filterDialog.show()

    def openRealTimeDialog(self):
        self.realTimeDialog.show()
