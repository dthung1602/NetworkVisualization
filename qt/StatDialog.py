from math import isnan, isinf

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QSizePolicy, QTabWidget
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

        self.layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.setCurrentIndex(0)
        self.selectStyle = self.findChild(QComboBox, 'selectStyle')
        self.selectEV = self.findChild(QComboBox, 'selectEV')
        self.selectAttr = self.findChild(QComboBox, 'selectAttr')
        self.centralityAttr = self.findChild(QComboBox, 'centralityAttr')
        self.centralityWeight = self.findChild(QComboBox, 'centralityWeight')

        self.styleOpt = 'bmh'
        self.ev = canvas.g.vs
        self.changeEV(0)
        self.comparableAttr = self.getComparableAttr()
        self.floatCentralityAttr = self.getFloatCentralityAttr()

        self.addSelectOptions()

    def addSelectOptions(self):
        # Edge / vertex
        self.selectEV.addItems(['Vertex', 'Edge'])
        self.selectEV.currentIndexChanged.connect(self.changeEV)
        # Attr
        self.selectAttr.currentIndexChanged.connect(self.changeAttr)
        # Graph Style Opt
        self.selectStyle.addItems([opt for opt in plt.style.available])
        self.selectStyle.currentIndexChanged.connect(self.changeStyle)

        # Centrality
        self.centralityAttr.addItems([opt[0] for opt in CENTRALITY_OPTIONS])
        self.centralityAttr.currentIndexChanged.connect(self.recalculateCentrality)
        self.centralityWeight.addItems(self.floatCentralityAttr)
        self.centralityWeight.currentIndexChanged.connect(self.recalculateCentrality)

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
        clearLayout(self.layout)
        ev = 'Vertices' if isinstance(self.ev, VertexSeq) else 'Edges'
        w = WidgetPlot(ev, attr, self.ev[attr], self.styleOpt)
        self.layout.addWidget(w)

    def changeStyle(self, opt):
        self.styleOpt = plt.style.available[opt]
        i = int(self.selectAttr.currentIndex())
        self.changeAttr(i)

    def recalculateCentrality(self, opt):
        centrality = CENTRALITY_OPTIONS[self.centralityAttr.currentIndex()]
        weight = self.floatCentralityAttr[self.centralityWeight.currentIndex()]
        values = getattr(self.canvas.g, centrality[1])(weights=weight)
        clearLayout(self.layout)
        w = WidgetPlot('Vertices', centrality[0], values, self.styleOpt)
        self.layout.addWidget(w)


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
