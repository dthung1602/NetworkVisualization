import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import igraph as ig
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from Canvas import Canvas


SELECT_PLOT = [
    ['Edge Weight'],
    ['Edge Speed Raw'],
    ['Degree Histogram'],

]


class Stat(QWidget):
    def __init__(self, canvas: Canvas):
        super().__init__()
        print('graph')
        self.canvas = canvas
        loadUi('resource/gui/StatDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Graph Generator")
        self.layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.selectPlot = self.findChild(QComboBox, 'selectPlot')
        self.addSelectOptions()
        self.edgeWeightPlot()

    def addSelectOptions(self):
        # Graph Layout Opt
        self.selectPlot.addItems([opt[0] for opt in SELECT_PLOT])
        self.selectPlot.currentIndexChanged.connect(self.changeGraphLayout)

    def changeGraphLayout(self, opt):
        switcher = {
            0: self.edgeWeightPlot,
            1: self.edgeSpeedPlot,
            2: self.degreeHistogram,
        }

        func = switcher.get(opt)
        func()

    def edgeWeightPlot(self):
        self.clearLayout(self.layout)
        weightArr = np.array(self.canvas.g.es['weight'])
        fig, ax1 = plt.subplots()
        num_bins = 15
        ax1.set_title('Edge Weights Histogram')
        ax1.set_xlabel('Number of Edges')
        ax1.set_ylabel('Weights')
        n, bins, patches = ax1.hist(weightArr, num_bins, facecolor='blue', alpha=0.5)
        graph = FigureCanvas(fig)
        self.layout.addWidget(graph)
        self.addToolBar(graph)

    def degreeHistogram(self):
        self.clearLayout(self.layout)
        weightArr = np.array(self.canvas.g.vs['degree'])
        fig, ax1 = plt.subplots()
        num_bins = 15
        ax1.set_title('Degree Distribution Histogram')
        ax1.set_xlabel('Degree')
        ax1.set_ylabel('Number of Vertex')
        n, bins, patches = ax1.hist(weightArr, num_bins, facecolor='blue', alpha=0.5)
        graph = FigureCanvas(fig)
        self.layout.addWidget(graph)
        self.addToolBar(graph)

    def edgeSpeedPlot(self):
        self.clearLayout(self.layout)
        weightArr = np.array(self.canvas.g.es['LinkSpeedRaw'])
        fig, ax1 = plt.subplots()
        num_bins = 10
        ax1.set_title('Link Speed Raw Histogram')
        ax1.set_xlabel('Number of Edges')
        ax1.set_ylabel('Speeds')
        n, bins, patches = ax1.hist(weightArr, num_bins, facecolor='blue', alpha=0.5)
        graph = FigureCanvas(fig)
        self.layout.addWidget(graph)
        self.addToolBar(graph)

    def addToolBar(self, graph):
        try:
            toolbar = NavigationToolbar(graph, self)
            toolbar.__delattr__("None")
            self.layout.addWidget(QtCore.Qt.BottomToolBarArea, toolbar)
        except Exception as e:
            print(e)

    @staticmethod
    def clearLayout(layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()
