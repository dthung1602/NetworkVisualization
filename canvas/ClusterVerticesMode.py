from igraph import VertexDendrogram

from .Mode import Mode
from .utils import randomColor

CLUSTERING_ALGO_OPTIONS = [
    ['Fast Greedy', 'community_fastgreedy'],
    ['Info Map', 'community_infomap'],
    ['Leading eigenvector', 'community_leading_eigenvector'],
    ['Label Propagation', 'community_label_propagation'],
    ['Multilevel', 'community_multilevel'],
    ['Optimal Modularity', 'community_optimal_modularity'],
    ['Edge Betweenness', 'community_edge_betweenness'],
    ['Spinglass', 'community_spinglass'],
    ['Walktrap', 'community_walktrap']
]


class ClusterVerticesMode(Mode):
    priority = 3
    conflict_modes = ['VertexAttrColorMode', 'CentralityMode']

    def __init__(self, gui):
        super().__init__(gui)
        self.weight = None
        self.clusterAlgo = 'community_fastgreedy'

    def onSet(self):
        if self.canvas.g:
            self.applyClusteringAlgo()

    def onSetGraph(self):
        g = self.canvas.g
        if 'cluster' not in g.vs.attributes():
            self.applyClusteringAlgo()
        else:
            clusterToColor = {cl: randomColor() for cl in set(g.vs['cluster'])}
            g.vs['color'] = [clusterToColor[v['cluster']] for v in g.vs]

    def applyClusteringAlgo(self):
        g = self.canvas.g
        clusterFunc = getattr(g, self.clusterAlgo)
        if self.clusterAlgo == 'community_infomap':
            clusters = clusterFunc(edge_weights=self.weight)
        else:
            clusters = clusterFunc(weights=self.weight)
        if isinstance(clusters, VertexDendrogram):
            clusters = clusters.as_clustering()
        clusters = clusters.subgraphs()

        def getClusterId(vertex):
            for cluster in clusters:
                if vertex['id'] in cluster.vs['id']:
                    return str(id(cluster))

        clusterToColor = {str(id(cl)): randomColor() for cl in clusters}
        g.vs['cluster'] = [getClusterId(v) for v in g.vs]
        g.vs['color'] = [clusterToColor[v['cluster']] for v in g.vs]
