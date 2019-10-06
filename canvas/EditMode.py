from PyQt5.QtCore import Qt

from .Mode import Mode


class EditMode(Mode):
    conflict_modes = ['ShortestPathMode', 'BottleNeckMode']
    priority = 1

    def __init__(self, gui):
        super().__init__(gui)
        self.addVertex = self.addEdge = self.deleteVertex = self.deleteEdge = False

    def onSet(self):
        self.canvas.selectedVertices = []
        self.canvas.selectedEdges = []

    def onUnset(self):
        self.addVertex = self.addEdge = self.deleteVertex = self.deleteEdge = False

    def onSetGraph(self):
        self.addVertex = self.addEdge = self.deleteVertex = self.deleteEdge = False

    def onSelectVertex(self, vertex):
        if self.deleteVertex:
            if vertex in self.canvas.selectedVertices:
                self.canvas.selectedVertices.remove(vertex)
            self.canvas.g.delete_vertices(vertex)
            self.deleteVertex = False
            return

        if self.addEdge:
            sv = self.canvas.selectedVertices
            if len(sv) == 2:
                self.canvas.selectedVertices = []
            sv.append(vertex)
            if len(sv) == 2:
                self.canvas.g.add_edge(sv[0], sv[1])
                self.canvas.selectedVertices = []
                self.addEdge = False
            return

        self.gui.displayVertex(vertex)
        self.canvas.selectedVertices = [vertex]
        self.canvas.selectedEdges = []

    def onSelectEdge(self, edge):
        if self.deleteEdge:
            if edge in self.canvas.selectedEdges:
                self.canvas.selectedEdges.remove(edge)
            self.canvas.g.delete_edges(edge)
            self.deleteEdge = False
            return

        self.gui.displayEdge(edge)
        self.canvas.selectedEdges = [edge]
        self.canvas.selectedVertices = []

    def onSelectBackground(self, pos):
        if self.addVertex:
            self.canvas.g.add_vertex(
                name=None,
                x=self.canvas.toAbsoluteX(pos.x()),
                y=self.canvas.toAbsoluteY(pos.y()),
                cluster=0,
                color=Qt.white,
                pos=pos,
            )
            self.addVertex = False

        super().onSelectBackground(pos)

    def onMouseMove(self, pos):
        if len(self.canvas.selectedVertices) > 0:
            vertex = self.canvas.selectedVertices[0]
            vertex['x'] = self.canvas.toAbsoluteX(pos.x())
            vertex['y'] = self.canvas.toAbsoluteY(pos.y())
