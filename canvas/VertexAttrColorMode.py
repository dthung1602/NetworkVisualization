from .Mode import Mode
from .utils import randomColor
from PyQt5.QtGui import QBrush

class VertexAttrColorMode(Mode):
    priority = 3
    conflict_modes = ['ClusterVerticesMode', 'CentralityMode']

    def __init__(self, gui):
        super().__init__(gui)
        self.attr = None

    def onSet(self):
        if self.canvas.g:
            self.applyAttrColor()

    def onSetGraph(self):
        if 'cluster' not in self.canvas.g.vs.attributes():
            self.applyAttrColor()
        else:
            clusterToColor = {cl: randomColor() for cl in set(self.canvas.g.vs['cluster'])}
            for v in self.canvas.g.vs:
                v['color'] = clusterToColor[v['cluster']]

    def applyAttrColor(self):
        g = self.canvas.g
        if self.attr is None:
            g.vs['cluster'] = [0] * g.vcount()
            g.vs['color'] = [randomColor()] * g.vcount()
        else:
            g.vs['cluster'] = g.vs[self.attr]
            clusterToColor = {cl: randomColor() for cl in set(g.vs[self.attr])}
            for v in g.vs:
                v['color'] = clusterToColor[v['cluster']]
