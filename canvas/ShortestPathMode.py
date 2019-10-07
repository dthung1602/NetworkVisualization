from .Mode import Mode


class ShortestPathMode(Mode):
    conflict_modes = ['EditMode', 'BottleNeckMode']
    priority = 1

    def __init__(self, gui):
        super().__init__(gui)
        self.weight = None
        self.src = self.dst = None

    def onSet(self):
        self.canvas.selectedVertices = []
        self.canvas.selectedEdges = []

    def onUpdateGraph(self):
        self.findShortestPath()

    def onSelectVertex(self, vertex):
        self.gui.displayVertex(vertex)
        canvas = self.canvas
        svl = len(canvas.selectedVertices)
        if svl != 1:
            canvas.selectedVertices = [vertex]
            canvas.selectedEdges = []
        else:
            canvas.selectedVertices.append(vertex)
            self.src, self.dst = canvas.selectedVertices
            self.findShortestPath()

    def findShortestPath(self):
        canvas = self.canvas
        g = canvas.g
        path = g.get_shortest_paths(
            self.src,
            self.dst,
            self.weight,
            output='epath'
        )
        if path[0]:
            canvas.selectedEdges = [g.es[i] for i in path[0]]
            canvas.selectedVertices = [g.vs[e.source] for e in canvas.selectedEdges] + [self.dst]
