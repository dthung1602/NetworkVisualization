import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QSizePolicy
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from canvas import Canvas
from .utils import clearLayout
# import figureOption

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
        self.selectPlot = self.findChild(QComboBox, 'selectPlot')
        self.styleOpt = 'bmh'
        self.addSelectOptions()
        self.edgeWeightPlot()

    def addSelectOptions(self):
        # Graph Style Opt
        self.selectStyle.addItems([opt for opt in plt.style.available])
        self.selectStyle.currentIndexChanged.connect(self.changeStyleLayout)
        # Graph Layout Opt
        self.selectPlot.addItems([opt[0] for opt in SELECT_PLOT])
        self.selectPlot.currentIndexChanged.connect(self.changeGraphLayout)

    def changeGraphLayout(self, opt):
        [
            self.edgeWeightPlot,
            self.edgeSpeedPlot,
            self.degreeHistogram,
        ][opt]()

    def changeStyleLayout(self, opt):
        self.styleOpt = plt.style.available[opt]
        i = int(self.selectPlot.currentIndex())
        self.changeGraphLayout(i)

    def edgeWeightPlot(self):
        clearLayout(self.layout)
        w = WidgetPlot(0, self.styleOpt, self.canvas)
        self.layout.addWidget(w)

    def edgeSpeedPlot(self):
        clearLayout(self.layout)
        w = WidgetPlot(1, self.styleOpt, self.canvas)
        self.layout.addWidget(w)

    def degreeHistogram(self):
        clearLayout(self.layout)
        w = WidgetPlot(2, self.styleOpt, self.canvas)
        self.layout.addWidget(w)


class WidgetPlot(QWidget):
    def __init__(self, opt, style: str, canvas: Canvas):
        super().__init__()
        self.canvas = canvas
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.plot = Plot(opt, style, self.canvas)
        self.toolbar = NavigationToolbar(self.plot, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.plot)


class Plot(FigureCanvas):
    def __init__(self, i: int, style: str, canvas: Canvas, parent=None, width=10, height=8, dpi=100):
        self.style = style
        self.canvas = canvas
        self.i = i
        fig = Figure()
        with plt.style.context(self.style):
            if i == 0:
                fig = self.edgeWeightPlot()
            elif i == 1:
                fig = self.edgeSpeedPlot()
            elif i == 2:
                fig = self.degreeHistogram()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.plot()

    def edgeWeightPlot(self):
        weightArr = np.array(self.canvas.g.es['weight'])
        fig, ax1 = plt.subplots()
        num_bins = 15
        ax1.set_title('Edge Weights Histogram')
        ax1.set_xlabel('Number of Edges')
        ax1.set_ylabel('Weights')
        n, bins, patches = ax1.hist(weightArr, num_bins)
        return fig

    def edgeSpeedPlot(self):
        weightArr = np.array(self.canvas.g.es['weight'])
        fig, ax1 = plt.subplots()
        num_bins = 10
        ax1.set_title('Link Speed Raw Histogram')
        ax1.set_xlabel('Number of Edges')
        ax1.set_ylabel('Speeds')
        n, bins, patches = ax1.hist(weightArr, num_bins)
        return fig

    def degreeHistogram(self):
        weightArr = np.array(self.canvas.g.vs['degree'])
        fig, ax1 = plt.subplots()
        num_bins = 15
        ax1.set_title('Degree Distribution Histogram')
        ax1.set_xlabel('Degree')
        ax1.set_ylabel('Number of Vertex')
        n, bins, patches = ax1.hist(weightArr, num_bins)
        return fig
