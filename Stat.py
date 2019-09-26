import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Filter import Filter
from Canvas import Canvas


class Stat(QDialog):
    def __init__(self, canvas: Canvas):
        super().__init__()
        print('graph')
        self.canvas = canvas
        loadUi('resource/gui/StatDialog.ui', self)
        self.setWindowIcon(QIcon('resource/gui/icon.ico'))
        self.setWindowTitle("Network Visualization - Team Black - Graph Generator")
        self.layout = self.findChild(QVBoxLayout, 'verticalLayout')
        self.plot()

    def plot(self):
        # test data
        x = [21, 22, 23, 4, 5, 6, 77, 8, 9, 10, 31, 32, 33, 34, 35, 36, 37, 18, 49, 50, 100]
        num_bins = 5
        fig, ax1 = plt.subplots()
        n, bins, patches = ax1.hist(x, num_bins, facecolor='blue', alpha=0.5)

        # data = np.array([0.7, 0.7, 0.7, 0.8, 0.9, 0.9, 1.5, 1.5, 1.5, 1.5])
        #
        # bins = np.arange(0.6, 1.62, 0.02)
        # n1, bins1, patches1 = ax1.hist(data, bins, alpha=0.6, density=False, cumulative=False)
        graph = FigureCanvas(fig)
        self.layout.addWidget(graph)
        try:
            self.layout.addWidget(QtCore.Qt.BottomToolBarArea, NavigationToolbar(graph, self))
        except Exception as e:
            print(e)
