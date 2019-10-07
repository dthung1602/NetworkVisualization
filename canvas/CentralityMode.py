from .Mode import Mode
from .utils import arrayToSpectrum

CENTRALITY_OPTIONS = [
    ['Closeness', 'closeness'],
    ['Betweenness', 'betweenness'],
    ['Eigenvector', 'evcent']
]


class CentralityMode(Mode):
    priority = 3
    conflict_modes = ['ClusterVerticesMode', 'VertexAttrColorMode']

    def __init__(self, gui):
        super().__init__(gui)
        self.centrality = None
        self.weight = None

    def onSet(self):
        if self.canvas.g:
            self.applyCentrality()

    def onSetGraph(self):
        self.applyCentrality()

    def onUpdateGraph(self):
        self.applyCentrality()

    def applyCentrality(self):
        centrality = getattr(self.canvas.g, self.centrality)(weights=self.weight)
        self.canvas.g.vs['color'] = arrayToSpectrum(centrality)
