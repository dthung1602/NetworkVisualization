from .Mode import Mode


class BottleNeckMode(Mode):
    priority = 1
    conflict_modes = ['EditMode', 'ShortestPathMode']

    def onSet(self):
        if self.canvas.g:
            self.findBottleNeck()

    def onSetGraph(self):
        self.findBottleNeck()

    def findBottleNeck(self):
        canvas = self.canvas
        g = canvas.g
        clusterOutgoingEdges = {cl: [] for cl in set(g.vs['cluster'])}
        for e in g.es:
            targetCluster = g.vs[e.target]['cluster']
            sourceCluster = g.vs[e.source]['cluster']
            if targetCluster != sourceCluster:
                clusterOutgoingEdges[targetCluster].append(e)
                clusterOutgoingEdges[sourceCluster].append(e)
        canvas.selectedEdges = []
        canvas.selectedVertices = []
        for cluster, edges in clusterOutgoingEdges.items():
            if len(edges) == 1:
                e = edges[0]
                canvas.selectedEdges.append(e)
                canvas.selectedVertices.append(g.vs[e.target])
                canvas.selectedVertices.append(g.vs[e.source])
