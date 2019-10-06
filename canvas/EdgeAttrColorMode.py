from PyQt5.QtGui import QPen

from .Mode import Mode
from .utils import arrayToSpectrum, randomColor


class EdgeAttrColorMode(Mode):
    priority = 3

    def __init__(self, gui):
        super().__init__(gui)
        self.attr = None

    def onSet(self):
        if self.canvas.g:
            self.setEdgesColor()

    def onSetGraph(self):
        self.setEdgesColor()

    def onUpdateGraph(self):
        self.setEdgesColor()

    def setEdgesColor(self):
        if self.attr is not None:
            self.canvas.g.es['color'] = arrayToSpectrum(self.canvas.g.es[self.attr])
        # else:
        #     self.canvas.g.es['color'] = [randomColor()] * self.canvas.g.ecount()
