from math import isnan, isinf

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QSizePolicy, QTabWidget, QLabel
from PyQt5.uic import loadUi
from igraph import VertexSeq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from canvas import Canvas, CENTRALITY_OPTIONS
from .utils import clearLayout


class StatDialog(QWidget):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self.canvas = canvas
        loadUi('resource/gui/StatDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Statistics")

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.setCurrentIndex(0)

        self.simpleAttrGraph = self.findChild(QVBoxLayout, 'simpleAttrGraph')
        self.selectStyleSA = self.findChild(QComboBox, 'selectStyleSA')
        self.selectEV = self.findChild(QComboBox, 'selectEV')
        self.selectAttr = self.findChild(QComboBox, 'selectAttr')
        self.styleSA = 'bmh'
        self.ev = canvas.g.vs

        self.computedAttrGraph = self.findChild(QVBoxLayout, 'computedAttrGraph')
        self.selectStyleCA = self.findChild(QComboBox, 'selectStyleCA')
        self.centralityAttr = self.findChild(QComboBox, 'centralityAttr')
        self.centralityWeight = self.findChild(QComboBox, 'centralityWeight')
        self.comparableAttr = self.getComparableAttr()
        self.styleCA = 'bmh'
        self.floatCentralityAttr = self.getFloatCentralityAttr()

        self.addSelectOptions()

        self.changeEV(0)
        self.recalculateCentrality(None)
        self.calculateSummary()

    def addSelectOptions(self):
        # Edge / vertex
        self.selectEV.addItems(['Vertex', 'Edge'])
        self.selectEV.currentIndexChanged.connect(self.changeEV)
        # Attr
        self.selectAttr.currentIndexChanged.connect(self.changeAttr)
        # Graph Style Opt
        self.selectStyleSA.addItems(plt.style.available)
        self.selectStyleSA.currentIndexChanged.connect(self.changeStyleSA)

        # Centrality
        self.centralityAttr.addItems([opt[0] for opt in CENTRALITY_OPTIONS])
        self.centralityAttr.currentIndexChanged.connect(self.recalculateCentrality)
        # Centrality weight
        self.centralityWeight.addItems(self.floatCentralityAttr)
        self.centralityWeight.currentIndexChanged.connect(self.recalculateCentrality)
        # Graph Style Opt
        self.selectStyleCA.addItems(plt.style.available)
        self.selectStyleCA.currentIndexChanged.connect(self.changeStyleCA)

    def calculateSummary(self):
        g = self.canvas.g
        componentCount = len(g.components().subgraphs())
        self.findChild(QLabel, 'totalE').setText(str(g.ecount()))
        self.findChild(QLabel, 'totalV').setText(str(g.vcount()))
        self.findChild(QLabel, 'componentCount').setText(str(componentCount))
        self.findChild(QLabel, 'isConnected').setText(str(componentCount == 1))
        self.findChild(QLabel, 'isMultigraph').setText(str(g.has_multiple()))
        self.findChild(QLabel, 'avgDegree').setText(str(np.mean(g.degree()))[:6])
        self.findChild(QLabel, 'density').setText(str(g.density())[:6])

    def getComparableAttr(self):
        def isStrOrFloat(v):
            return isinstance(v, str) or isinstance(v, float)

        return [attr for attr in self.ev.attributes() if isStrOrFloat(self.ev[0][attr])]

    def getFloatCentralityAttr(self):
        es = self.canvas.g.es
        return [attr for attr in es.attributes() if isinstance(es[0][attr], float)]

    def changeEV(self, opt):
        self.ev = getattr(self.canvas.g, ['vs', 'es'][opt])
        self.comparableAttr = self.getComparableAttr()
        self.selectAttr.clear()
        self.selectAttr.addItems(self.comparableAttr)
        self.changeAttr(0)

    def changeAttr(self, opt):
        attr = self.comparableAttr[opt]
        clearLayout(self.simpleAttrGraph)
        ev = 'Vertices' if isinstance(self.ev, VertexSeq) else 'Edges'
        w = WidgetPlot(ev, attr, self.ev[attr], self.styleSA)
        self.simpleAttrGraph.addWidget(w)

    def changeStyleSA(self, opt):
        self.styleSA = plt.style.available[opt]
        i = int(self.selectAttr.currentIndex())
        self.changeAttr(i)

    def recalculateCentrality(self, opt):
        centrality = CENTRALITY_OPTIONS[self.centralityAttr.currentIndex()]
        weight = self.floatCentralityAttr[self.centralityWeight.currentIndex()]
        values = getattr(self.canvas.g, centrality[1])(weights=weight)
        clearLayout(self.computedAttrGraph)
        w = WidgetPlot('Vertices', centrality[0], values, self.styleCA)
        self.computedAttrGraph.addWidget(w)

    def changeStyleCA(self, opt):
        self.styleCA = plt.style.available[opt]
        self.recalculateCentrality(None)


class WidgetPlot(QWidget):
    def __init__(self, ev, attr, values, style):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.plot = Plot(ev, attr, values, style)
        self.toolbar = NavigationToolbar(self.plot, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.plot)


class Plot(FigureCanvas):
    def __init__(self, ev, attr, values, style):
        with plt.style.context(style):
            weightArr = list(filter(lambda x: isinstance(x, str) or not (isnan(x) or isinf(x)), values))
            fig, ax = plt.subplots()
            num_bins = 30
            ax.set_title(attr + ' distribution')
            ax.set_ylabel('Number of ' + ev)
            ax.set_xlabel(attr)
            if weightArr and isinstance(weightArr[0], float):
                meanLine = ax.axvline(np.mean(weightArr), color='r', linestyle='--')
                medianLine = ax.axvline(np.median(weightArr), color='b', linestyle='-')
                plt.legend([meanLine, medianLine], ['Mean', 'Median'])
            ax.hist(weightArr, num_bins)

        FigureCanvas.__init__(self, fig)
        self.setParent(None)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
