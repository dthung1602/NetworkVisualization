from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QWidget, QPushButton, QLineEdit, QLabel, QTabWidget
from PyQt5.uic import loadUi

from canvas import *


class FilterDialog(QWidget):
    def __init__(self, canvas: Canvas, layoutMode: LayoutMode, clusterMode: ClusterVerticesMode,
                 centralityMode: CentralityMode, vertexAttrMode: VertexAttrColorMode,
                 edgeAttrMode: EdgeAttrColorMode, filterEdgeMode: FilterEdgeMode):
        super().__init__()
        self.canvas = canvas
        self.layoutMode = layoutMode
        self.clusterMode = clusterMode
        self.centralityMode = centralityMode
        self.vertexAttrMode = vertexAttrMode
        self.edgeAttrMode = edgeAttrMode
        self.filterEdgeMode = filterEdgeMode

        loadUi('resource/gui/FilterDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Filter Dialog")
        self.tab = self.findChild(QTabWidget, 'tabWidget')
        self.tab.setCurrentIndex(0)
        self.vertexAttr = [opt for opt in self.canvas.g.vs.attributes()]

        self.edgeWeights = [opt for opt in self.canvas.g.es.attributes()]
        self.edgeWeights.remove('line')

        self.selectLayout = self.findChild(QComboBox, 'selectLayout')
        self.selectLayoutEdgeWeight = self.findChild(QComboBox, 'selectLayoutEdgeWeight')
        self.labelLayoutEdgeWeight = self.findChild(QLabel, 'labelLayoutEdgeWeight')
        self.applyLayoutBtn = self.findChild(QPushButton, 'applyLayoutBtn')

        self.selectClusteringAlgo = self.findChild(QComboBox, 'selectClusteringAlgo')
        self.selectClusteringAlgoEdgeWeight = self.findChild(QComboBox, 'selectClusteringAlgoEdgeWeight')
        self.applyClusterBtn = self.findChild(QPushButton, 'applyClusterBtn')

        self.selectFilterEdge = self.findChild(QComboBox, 'selectFilterEdge')
        self.applyFilterBtn = self.findChild(QPushButton, 'applyFilterBtn')
        self.filterLeft = self.findChild(QLineEdit, 'filterLeft')
        self.filterRight = self.findChild(QLineEdit, 'filterRight')

        self.selectCentrality = self.findChild(QComboBox, 'selectCentrality')
        self.selectCentralityEdgeWeight = self.findChild(QComboBox, 'selectCentralityEdgeWeight')
        self.applyCentralityBtn = self.findChild(QPushButton, 'applyCentralityBtn')
        self.cancelCentralityBtn = self.findChild(QPushButton, 'cancelCentralityBtn')

        self.selectClusterAttribute = self.findChild(QComboBox, 'selectVertex')
        self.applyClusterAttribute = self.findChild(QPushButton, 'applyVertexBtn')

        self.selectEdgeAttribute = self.findChild(QComboBox, 'selectEdge')
        self.applyEdgeAttribute = self.findChild(QPushButton, 'applyEdge')
        self.addSelectOptions()
        self.setShowLayoutWeight(0)

    def addSelectOptions(self):
        # Graph Layout Opt
        self.selectLayout.addItems([opt[0] for opt in LAYOUT_OPTIONS])
        self.selectLayout.currentIndexChanged.connect(self.setShowLayoutWeight)
        self.selectLayoutEdgeWeight.addItems(['-- Please choose --'] + self.edgeWeights)
        self.applyLayoutBtn.pressed.connect(self.changeGraphLayout)

        # Clustering Algo Opt
        self.selectClusteringAlgo.addItems([opt[0] for opt in CLUSTERING_ALGO_OPTIONS])
        self.selectClusteringAlgoEdgeWeight.addItems(['-- Please choose --'] + self.edgeWeights)
        self.applyClusterBtn.pressed.connect(self.changeClusteringAlgo)

        # Filter Edge Opt
        self.selectFilterEdge.addItems(self.edgeWeights)
        self.applyFilterBtn.pressed.connect(self.changeEdgeFilter)

        # Centrality
        self.selectCentrality.addItems([opt[0] for opt in CENTRALITY_OPTIONS])
        self.selectCentralityEdgeWeight.addItems(['-- Please choose --'] + self.edgeWeights)
        self.applyCentralityBtn.pressed.connect(self.changeCentrality)
        self.cancelCentralityBtn.pressed.connect(self.cancelCentrality)

        # Cluster Attribute Opt
        self.selectClusterAttribute.addItems(self.vertexAttr)
        self.applyClusterAttribute.pressed.connect(self.changeClusterAttribute)

        # Edge Attribute Opt
        self.selectEdgeAttribute.addItems(['-- Please choose --'] + self.canvas.g.es.attributes())
        self.applyEdgeAttribute.pressed.connect(self.setEdgeAttr)

    def setShowLayoutWeight(self, opt):
        visible = LAYOUT_OPTIONS[opt][1] in LAYOUT_WITH_WEIGHT
        self.selectLayoutEdgeWeight.setVisible(visible)
        self.labelLayoutEdgeWeight.setVisible(visible)

    def setEdgeAttr(self):
        opt = self.selectEdgeAttribute.currentIndex()
        attr = self.canvas.g.es.attributes()[opt - 1] if opt > 0 else None
        self.edgeAttrMode.attr = attr
        self.canvas.addMode(self.edgeAttrMode)

    def changeGraphLayout(self):
        layout = LAYOUT_OPTIONS[self.selectLayout.currentIndex()][1]
        i = self.selectLayoutEdgeWeight.currentIndex()
        weight = self.edgeWeights[i - 1] if i > 0 else None
        self.layoutMode.setLayout(layout, weight)

    def changeClusteringAlgo(self):
        algo = CLUSTERING_ALGO_OPTIONS[self.selectClusteringAlgo.currentIndex()][1]
        i = self.selectClusteringAlgoEdgeWeight.currentIndex()
        weight = self.edgeWeights[i - 1] if i > 0 else None
        self.clusterMode.clusterAlgo = algo
        self.clusterMode.weight = weight
        self.canvas.addMode(self.clusterMode)

    def changeEdgeFilter(self):
        attr = self.edgeWeights[self.selectFilterEdge.currentIndex()]
        left = float(self.filterLeft.text())
        right = float(self.filterRight.text())
        self.filterEdgeMode.setFilters(attr, left, right)

    def changeCentrality(self):
        centrality = CENTRALITY_OPTIONS[self.selectCentrality.currentIndex()][1]
        i = self.selectCentralityEdgeWeight.currentIndex()
        weight = self.edgeWeights[i - 1] if i > 0 else None
        self.centralityMode.centrality = centrality
        self.centralityMode.weight = weight
        self.canvas.addMode(self.centralityMode)

    def cancelCentrality(self):
        self.changeClusteringAlgo()

    def changeClusterAttribute(self):
        attr = self.vertexAttr[self.selectClusterAttribute.currentIndex()]
        self.vertexAttrMode.attr = attr
        self.canvas.addMode(self.vertexAttrMode)
