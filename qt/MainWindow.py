import igraph
from PIL import Image
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import *
from igraph import Graph

from canvas import *
from .AboutUsDialog import AboutUsDialog
from .AddAttributesDialog import AddAttributesDialog
from .ConstraintDialog import ConstraintDialog
from .FilterDialog import FilterDialog
from .InfoWidget import EdgeInfoWidget, VertexInfoWidget
from .RealTimeDialog import *
from .ShortestPathWeightDialog import ShortestPathWeightDialog
from .StatDialog import StatDialog
from .utils import clearLayout

DEFAULT_GRAPH = 'resource/graph/NREN.graphml'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('resource/gui/GUI.ui', self)

        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black")
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)

        self.canvas = Canvas(1129, 760)
        self.findChild(QVBoxLayout, 'verticalLayout').addWidget(self.canvas)

        # Modes
        # 0
        self.darkMode = DarkViewMode(self)
        self.lightMode = LightViewMode(self)
        self.geoMode = GeoViewMode(self)
        # 1
        self.editMode = EditMode(self)
        self.shortestPathMode = ShortestPathMode(self)
        self.bottleNeckMode = BottleNeckMode(self)
        # 2
        self.layoutMode = LayoutMode(self)
        # 3
        self.clusterVerticesMode = ClusterVerticesMode(self)
        self.centralityMode = CentralityMode(self)
        self.vertexAttrColorMode = VertexAttrColorMode(self)
        self.edgeAttrColorMode = EdgeAttrColorMode(self)
        self.filterEdgeMode = FilterEdgeMode(self)
        # 4
        self.realTimeMode = RealTimeMode(self)

        defaultModes = [
            self.darkMode,
            self.editMode,
            self.layoutMode,
            self.clusterVerticesMode,
            self.edgeAttrColorMode,
            self.filterEdgeMode
        ]
        for m in defaultModes:
            self.canvas.addMode(m)
        self.canvas.setGraph(DEFAULT_GRAPH)

        self.realTimeDialog = self.statDialog = self.filterDialog = None

        self.infoArea = self.findChild(QVBoxLayout, 'infoArea')
        self.bindMenuActions()

    def bindMenuActions(self):
        # ------------- Menu ---------------- #
        # File
        # Open_button
        openBtn = self.findChild(QAction, 'action_Open')
        openBtn.triggered.connect(self.openFileNameDialog)
        # Open_Image
        openImageBtn = self.findChild(QAction, 'actionOpen_Image')
        openImageBtn.triggered.connect(self.openImageToGraphDialog)
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
        # About Us
        aboutUsBtn = self.findChild(QAction, 'actionAboutUs')
        aboutUsBtn.triggered.connect(self.aboutUsDialog)
        # View
        # Zoom in
        self.findChild(QAction, 'actionZoom_In').triggered.connect(self.canvas.zoomInEvent)
        # Zoom out
        self.findChild(QAction, 'actionZoom_Out').triggered.connect(self.canvas.zoomOutEvent)
        # Zoom reset
        self.findChild(QAction, 'actionReset_Zoom').triggered.connect(self.canvas.zoomResetEvent)
        # View mode
        self.findChild(QAction, 'actionGeographical_Mode').triggered.connect(self.changeViewModeTo(GeoViewMode))
        self.findChild(QAction, 'actionDark_Mode').triggered.connect(self.changeViewModeTo(DarkViewMode))
        self.findChild(QAction, 'actionLight_Mode').triggered.connect(self.changeViewModeTo(LightViewMode))

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
        addVertexBtn.pressed.connect(self.editMode.setAddVertex)
        # Delete Vertex
        deleteBtn = self.findChild(QToolButton, 'delete_node_btn')
        deleteBtn.pressed.connect(self.editMode.setDeleteVertex)
        # Add Line
        addLineBtn = self.findChild(QToolButton, 'add_line_btn')
        addLineBtn.pressed.connect(self.editMode.setAddEdge)
        # Delete Line
        deleteLineBtn = self.findChild(QToolButton, 'delete_line_btn')
        deleteLineBtn.pressed.connect(self.editMode.setDeleteEdge)

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
        AddAttributesDialog(self.canvas).exec()

    def openConstraintDialog(self):
        constraintDialog = ConstraintDialog(self.canvas)
        constraintDialog.exec()
        constraintDialog.check()

    def changeViewModeTo(self, viewModeClass):
        def func():
            self.canvas.addMode(viewModeClass(self))
            self.canvas.resetViewRect()
            self.canvas.update()

        return func

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

    def openImageToGraphDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "./resource/graph",
            "All Files (*);;Python Files (*.py)", options=options
        )
        if fileName:
            img = Image.open(fileName, "r")
            w, h = img.size
            MAX_WIDTH = 160
            if w > MAX_WIDTH:
                wpercent = (MAX_WIDTH * 1.0 / w)
                hsize = int(h * wpercent)
                img = img.resize((MAX_WIDTH, hsize), Image.ANTIALIAS)
                w, h = img.size
            data = img.load()
            graph = Graph()
            for i in range(h):
                for j in range(w):
                    if img.mode == 'RGBA':
                        r, g, b, a = data[j, i]
                        color = QColor(r, g, b).name()
                        if a > 0:
                            graph.add_vertex(
                                x=j,
                                y=i,
                                color=color
                            )
                    elif img.mode == 'RGB':
                        r, g, b = data[j, i]
                        color = QColor(r, g, b).name()
                        graph.add_vertex(
                            x=j,
                            y=i,
                            color=color
                        )
            self.canvas.setGraph(graph)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "",
            "All Files (*);;GraphML Files (*.graphml);;GML Files (*.gml)", options=options
        )

        # process graph before saving
        g = self.canvas.g.copy()
        g.vs['color'] = [c.name() if isinstance(c, QColor) else c.color().name() for c in g.vs['color']]
        g.es['color'] = [c.name() if isinstance(c, QColor) else c.color().name() for c in g.es['color']]
        del g.es['line']
        del g.vs['pos']

        if fileName:
            if ".graphml" in fileName:
                g.write_graphml(fileName)
            elif ".gml" in fileName:
                g.write_gml(fileName)

    def activateFindShortestPathMode(self):
        ShortestPathWeightDialog(self.canvas, self.shortestPathMode).exec()
        self.canvas.addMode(self.shortestPathMode)

    def activateEditGraphMode(self):
        self.canvas.addMode(self.editMode)

    def activateFindBottleNeckMode(self):
        self.canvas.addMode(self.bottleNeckMode)

    def displayVertex(self, vertex):
        clearLayout(self.infoArea)
        vertexInfo = VertexInfoWidget(vertex, self.canvas)
        self.infoArea.addWidget(vertexInfo)

    def displayEdge(self, edge):
        clearLayout(self.infoArea)
        edgeInfo = EdgeInfoWidget(edge, self.canvas)
        self.infoArea.addWidget(edgeInfo)

    def clearInfoArea(self):
        clearLayout(self.infoArea)

    def openStatDialog(self):
        self.statDialog = StatDialog(self.canvas)
        self.statDialog.show()

    def openFilterDialog(self):
        self.filterDialog = FilterDialog(
            self.canvas,
            self.layoutMode,
            self.clusterVerticesMode,
            self.centralityMode,
            self.vertexAttrColorMode,
            self.edgeAttrColorMode,
            self.filterEdgeMode
        )
        self.filterDialog.show()

    @staticmethod
    def aboutUsDialog():
        aboutUsWindow = AboutUsDialog()
        aboutUsWindow.exec()

    def openRealTimeDialog(self):
        self.realTimeDialog = RealTimeDialog(self.canvas, self.realTimeMode)
        self.realTimeDialog.show()
