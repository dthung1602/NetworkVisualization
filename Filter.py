from PyQt5.QtGui import QIcon, QWindow
from PyQt5.QtWidgets import QDialog, QComboBox
from PyQt5.uic import loadUi

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


class Filter(QDialog):
    def __init__(self, canvas):
        super().__init__()
        print('Filter Dialog')
        self.canvas = canvas
        loadUi('resource/gui/FilterDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Filter Dialog")

        self.selectLayout = self.findChild(QComboBox, 'selectLayout')
        self.selectClusteringAlgo = self.findChild(QComboBox, 'selectClusteringAlgo')

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

    