from math import isnan, isinf

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QSizePolicy
from PyQt5.uic import loadUi
from igraph import VertexSeq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from canvas import Canvas
from .utils import clearLayout

SELECT_PLOT = [
    ['Edge Weight'],
    ['Edge Speed Raw'],
    ['Degree Histogram'],
]


class StatDialog(QWidget):
    def __init__(self, canvas: Canvas):
        super().__init__()
        self.canvas = canvas
        loadUi('resource/gui/StatDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Graph Generator")

        self.layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.selectStyle = self.findChild(QComboBox, 'selectStyle')
        self.selectEV = self.findChild(QComboBox, 'selectEV')
        self.selectAttr = self.findChild(QComboBox, 'selectAttr')

        self.styleOpt = 'bmh'
        self.ev = canvas.g.vs
        self.changeEV(0)
        self.comparableAttr = self.getComparableAttr()

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

    def getComparableAttr(self):
        def isStrOrFloat(v):
            return isinstance(v, str) or isinstance(v, float)

        return [attr for attr in self.ev.attributes() if isStrOrFloat(self.ev[0][attr])]

    def changeEV(self, opt):
        self.ev = getattr(self.canvas.g, ['vs', 'es'][opt])
        self.comparableAttr = self.getComparableAttr()
        self.selectAttr.clear()
        self.selectAttr.addItems(self.comparableAttr)
        self.changeAttr(0)

    def changeAttr(self, opt):
        attr = self.comparableAttr[opt]
        clearLayout(self.layout)
        w = WidgetPlot(self.ev, attr, self.styleOpt, self.canvas)
        self.layout.addWidget(w)

    def changeStyle(self, opt):
        self.styleOpt = plt.style.available[opt]
        i = int(self.selectAttr.currentIndex())
        self.changeAttr(i)


class WidgetPlot(QWidget):
    def __init__(self, ev, attr: str, style: str, canvas: Canvas):
        super().__init__()
        self.canvas = canvas
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.plot = Plot(ev, attr, style)
        self.toolbar = NavigationToolbar(self.plot, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.plot)


class Plot(FigureCanvas):
    def __init__(self, ev, attr: str, style: str):
        evStr = 'vertices' if isinstance(ev, VertexSeq) else 'edges'

        with plt.style.context(style):
            weightArr = list(filter(lambda x: isinstance(x, str) or not (isnan(x) or isinf(x)), ev[attr]))
            fig, ax = plt.subplots()
            num_bins = 20
            ax.set_title(attr + ' distribution')
            ax.set_ylabel('Number of ' + evStr)
            ax.set_xlabel(attr)
            if weightArr and isinstance(weightArr[0], float):
                meanLine= ax.axvline(np.mean(weightArr), color='r', linestyle='--')
                medianLine = ax.axvline(np.median(weightArr), color='b', linestyle='-')
                plt.legend([meanLine, medianLine], ['Mean', 'Median'])
            ax.hist(weightArr, num_bins)

        FigureCanvas.__init__(self, fig)
        self.setParent(None)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
