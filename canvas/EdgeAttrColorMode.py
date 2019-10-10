from PyQt5.QtGui import QPen

from .Mode import Mode
from .utils import arrayToSpectrum, randomColor


class EdgeAttrColorMode(Mode):
    priority = 3

    def __init__(self, gui):
        super().__init__(gui)
        self.attr = None

    def onSet(self):
        self.gui.spectrum.show()
        if self.canvas.g:
            self.setEdgesColor()

    def onUnset(self):
        self.gui.spectrum.hide()

    def onSetGraph(self):
        self.setEdgesColor()

    def onUpdateGraph(self):
        self.setEdgesColor()

    def setEdgesColor(self):
        if self.attr is not None:
            self.canvas.g.es['color'] = [QPen(c, 2) for c in arrayToSpectrum(self.canvas.g.es[self.attr])]
        # else:
        #     self.canvas.g.es['color'] = [randomColor()] * self.canvas.g.ecount()
