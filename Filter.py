from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.uic import loadUi

from Canvas import Canvas

LAYOUT_OPTIONS = [
    ['Bipartite', 'layout_bipartite'],
    ['Circle', 'layout_circle'],
    ['Distributed Recursive', 'layout_drl'],
    ['Fruchterman-Reingold', 'layout_fruchterman_reingold'],
    ['Graphopt', 'layout_graphopt'],
    ['Grid', 'layout_grid'],
    ['Kamada-Kawai', 'layout_kamada_kawai'],
    ['Large Graph', 'layout_lgl'],
    ['MDS', 'layout_mds'],
    ['Random', 'layout_random'],
    ['Reingold-Tilford', 'layout_reingold_tilford'],
    ['Reingold-Tilford Circular', 'layout_reingold_tilford_circular'],
    ['Star', 'layout_star']
]

LAYOUT_WITH_WEIGHT = ['layout_drl', 'layout_fruchterman_reingold']

CLUSTERING_ALGO_OPTIONS = [
    ['Fast Greedy', 'community_fastgreedy'],
    ['Info Map', 'community_infomap'],
    ['Leading eigenvector', 'community_leading_eigenvector'],
    ['Label Propagation', 'community_label_propagation'],
    ['Multilevel', 'community_multilevel'],
    ['Optimal Modularity', 'community_optimal_modularity'],
    ['Edge Betweenness', 'community_edge_betweenness'],
    ['Spinglass', 'community_spinglass'],
    ['Walktrap', 'community_walktrap']
]


class Filter(QWidget):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self.canvas = canvas

        loadUi('resource/gui/FilterDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Filter Dialog")

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

        self.addSelectOptions()
        self.setShowLayoutWeight(0)

    def addSelectOptions(self):
        # Graph Layout Opt
        self.selectLayout.addItems([opt[0] for opt in LAYOUT_OPTIONS])
        self.selectLayout.currentIndexChanged.connect(self.setShowLayoutWeight)
        self.selectLayoutEdgeWeight.addItems(['-- None --'] + self.edgeWeights)
        self.applyLayoutBtn.pressed.connect(self.changeGraphLayout)

        # Clustering Algo Opt
        self.selectClusteringAlgo.addItems([opt[0] for opt in CLUSTERING_ALGO_OPTIONS])
        self.selectClusteringAlgoEdgeWeight.addItems(['-- None --'] + self.edgeWeights)
        self.applyClusterBtn.pressed.connect(self.changeClusteringAlgo)

        # Filter Edge Opt
        self.selectFilterEdge.addItems(self.edgeWeights)
        self.applyFilterBtn.pressed.connect(self.changeFilterEdge)

    def setShowLayoutWeight(self, opt):
        visible = LAYOUT_OPTIONS[opt][1] in LAYOUT_WITH_WEIGHT
        self.selectLayoutEdgeWeight.setVisible(visible)
        self.labelLayoutEdgeWeight.setVisible(visible)

    def changeGraphLayout(self):
        layout = LAYOUT_OPTIONS[self.selectLayout.currentIndex()][1]
        i = self.selectLayoutEdgeWeight.currentIndex()
        weight = self.edgeWeights[i - 1] if i > 0 else None
        self.canvas.setGraphLayout(layout, weight)

    def changeClusteringAlgo(self):
        algo = CLUSTERING_ALGO_OPTIONS[self.selectClusteringAlgo.currentIndex()][1]
        i = self.selectClusteringAlgoEdgeWeight.currentIndex()
        weight = self.edgeWeights[i - 1] if i > 0 else None
        self.canvas.setClusteringAlgo(algo, weight)

    def changeFilterEdge(self):
        attr = self.edgeWeights[self.selectFilterEdge.currentIndex()]
        left = float(self.filterLeft.text())
        right = float(self.filterRight.text())
        self.canvas.setFilter(attr, left, right)
