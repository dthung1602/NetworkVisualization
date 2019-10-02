import threading
import time

import igraph
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from igraph import VertexDendrogram
from numpy import *

from utils import *


class Canvas(QWidget):
    WIDTH = 1120
    HEIGHT = 760

    SCREEN_RECT_LINE = [
        QLineF(0, 0, WIDTH, 0),
        QLineF(WIDTH, 0, WIDTH, HEIGHT),
        QLineF(WIDTH, HEIGHT, 0, HEIGHT),
        QLineF(0, HEIGHT, 0, 0)
    ]

    SCREEN_RECT = QRectF(0, 0, WIDTH, HEIGHT)

    POINT_RADIUS = 8
    SELECTED_POINT_RADIUS = 12
    LINE_DISTANCE = 2
    CURVE_SELECT_SQUARE_SIZE = 10

    DEFAULT_GRAPH = 'resource/graph/NREN-delay.graphml'
    DEFAULT_CLUSTERING_ALGO = 'community_edge_betweenness'
    DEFAULT_GRAPH_LAYOUT = 'layout_circle'

    MODE_EDIT = 'edit'
    MODE_FIND_SHORTEST_PATH = 'fsp'
    MODE_FIND_BOTTLE_NECK = 'fbn'
    MODE_REAL_TIME = 'rt'

    initModeAction = {
        MODE_FIND_BOTTLE_NECK: 'findBottleNeck'
    }

    def __init__(self, gui):
        super().__init__(None)
        self.gui = gui

        self.mode = self.MODE_EDIT
        self.viewMode = DARK_MODE

        self.g = self.clusterToColor = None
        self.addNode = self.deleteNode = self.addLine = self.deleteLine = None
        self.filterData = None

        self.center = self.zoom = self.viewRect = self.backgroundRect = self.pointsToDraw = self.linesToDraw = None
        self.backgroundDragging = self.pointDragging = None
        self.selectedLines = self.selectedPoints = []
        self.backGroundImage = self.backgroundColor = self.lineColor = None
        self.shortestPathWeight = None
        self.threading = None
        self.inRealTimeMode = None

        self.setGraph(self.DEFAULT_GRAPH)
        self.setViewMode(DARK_MODE)
        self.vertexDegree()

    def setMode(self, mode):
        self.mode = mode
        self.selectedPoints = []
        self.selectedLines = []
        initAction = self.initModeAction.get(mode)
        if initAction:
            getattr(self, initAction)()
        self.update()

    def setViewMode(self, viewMode):
        self.viewMode = viewMode
        if viewMode == DARK_MODE:
            self.backgroundColor = Qt.black
            self.lineColor = Qt.white
            self.g.es['color'] = [Qt.white] * self.g.ecount()
        elif viewMode == LIGHT_MODE:
            self.backgroundColor = Qt.white
            self.lineColor = Qt.black
            self.g.es['color'] = [Qt.black] * self.g.ecount()
        elif self.backGroundImage is None:
            self.backGroundImage = QImage('resource/gui/maptovl.png')
            self.lineColor = Qt.red
        self.resetViewRect()

    def setGraph(self, g):
        if isinstance(g, str):
            g = igraph.read(g)
        self.g = g
        self.vertexDegree()

        vsAttributes = g.vs.attributes()
        if 'x' not in vsAttributes or 'y' not in vsAttributes:
            self.setGraphLayout(self.DEFAULT_GRAPH_LAYOUT, None)
        if 'cluster' not in vsAttributes:
            self.setClusteringAlgo(self.DEFAULT_CLUSTERING_ALGO, None)
        else:
            clusterToColor = {cluster: randomColor() for cluster in set(g.vs['cluster'])}
            g.vs['color'] = [clusterToColor[cluster] for cluster in g.vs['cluster']]
        self.resetViewRect()

    def geolocationToXY(self, longitude, latitude):
        x = (longitude + 180) * (self.WIDTH / 360)
        latRad = radians(latitude)
        mercN = log(tan((pi / 4) + (latRad / 2)))
        y = (self.HEIGHT / 2) - (self.WIDTH * mercN / (2 * pi))
        return x, y

    def resetViewRect(self):
        g = self.g

        if self.viewMode == GEO_MODE:
            for v in g.vs:
                longitude = v['Longitude']
                latitude = v['Latitude']
                if isnan(longitude) or isnan(latitude):
                    v['x'] = self.WIDTH / 2
                    v['y'] = self.HEIGHT / 2 + 150
                else:
                    x, y = self.geolocationToXY(longitude, latitude)
                    v['x'] = x
                    v['y'] = y + 150
        else:
            # use translation to convert negative coordinates to non-negative
            mx = min(g.vs['x']) - 1
            my = min(g.vs['y']) - 1
            g.vs['x'] = [x - mx for x in g.vs['x']]
            g.vs['y'] = [y - my for y in g.vs['y']]

            mx = max(g.vs['x'])
            my = max(g.vs['y'])
            scale = self.WIDTH / mx if mx / my > self.WIDTH / self.HEIGHT else self.HEIGHT / my

            # convert init coordinates to coordinates on window
            g.vs['x'] = [x * scale for x in g.vs['x']]
            g.vs['y'] = [y * scale for y in g.vs['y']]

        # Init
        self.backgroundDragging = self.pointDragging = None
        self.selectedLines = self.selectedPoints = []
        self.center = QPointF(self.WIDTH / 2, self.HEIGHT / 2)
        self.zoom = 1
        self.viewRect = self.pointsToDraw = self.linesToDraw = None
        self.updateViewRect()

    def setGraphLayout(self, layoutName, weights):
        layoutFunc = getattr(self.g, layoutName)
        if layoutName in LAYOUT_WITH_WEIGHT:
            layout = layoutFunc(weights=weights)
        else:
            layout = layoutFunc()
        for c, v in zip(layout.coords, self.g.vs):
            v['x'] = c[0]
            v['y'] = c[1]
        self.resetViewRect()
        self.update()

    def setClusteringAlgo(self, algoName, weights):
        clusterFunc = getattr(self.g, algoName)
        if algoName == 'community_infomap':
            clusters = clusterFunc(edge_weights=weights)
        else:
            clusters = clusterFunc(weights=weights)
        if isinstance(clusters, VertexDendrogram):
            clusters = clusters.as_clustering()
        clusters = clusters.subgraphs()

        def getClusterId(vertex):
            for cluster in clusters:
                if vertex['id'] in cluster.vs['id']:
                    return str(id(cluster))

        clusterToColor = {str(id(cl)): randomColor() for cl in clusters}
        self.g.vs['cluster'] = [getClusterId(v) for v in self.g.vs]
        self.g.vs['color'] = [clusterToColor[v['cluster']] for v in self.g.vs]
        self.update()

    def setAttributeCluster(self, attr):
        cluster = {i: [] for i in self.g.vs[attr]}
        clusterToColor = {cl: randomColor() for cl in cluster.keys()}
        for i in cluster.keys():
            for v in self.g.vs:
                if v[attr] == i:
                    v['color'] = clusterToColor[i]
        self.update()

    def setFilter(self, attr='total_delay', left=0, right=54):
        self.filterData = {'attr': attr, 'left': left, 'right': right}
        self.update()

    def setCentrality(self, centrality, weights):
        centrality = getattr(self.g, centrality)(weights=weights)
        self.g.vs['color'] = arrayToSpectrum(centrality)

    def setEdgeColor(self):
        self.g.es['color'] = arrayToSpectrum(self.g.es['total_delay'])


    def updateViewRect(self):
        viewRectWidth = self.WIDTH / self.zoom
        viewRectHeight = self.HEIGHT / self.zoom
        viewRectX = self.center.x() - viewRectWidth / 2
        viewRectY = self.center.y() - viewRectHeight / 2
        self.viewRect = QRectF(viewRectX, viewRectY, viewRectWidth, viewRectHeight)

        if self.backGroundImage:
            scale = self.backGroundImage.width() / self.WIDTH
            self.backgroundRect = QRectF(viewRectX * scale, viewRectY * scale,
                                         viewRectWidth * scale, viewRectHeight * scale)

        def intersectWithViewRect(line):
            if isinstance(line, QLineF):
                return any([line.intersect(vrl, QPointF()) == 1 for vrl in self.SCREEN_RECT_LINE])
            return line.intersects(self.SCREEN_RECT)

        def inScreen(edge):
            return self.SCREEN_RECT.contains(self.g.vs[edge.source]['pos']) or self.SCREEN_RECT.contains(
                self.g.vs[edge.target]['pos'])

        self.g.vs['pos'] = [QPointF(
            (v['x'] - viewRectX) * self.zoom,
            (v['y'] - viewRectY) * self.zoom
        ) for v in self.g.vs]

        multipleEdge = {}
        for e in self.g.es:
            count = e.count_multiple()
            if count > 1:
                p1 = self.g.vs[e.source]['pos']
                p2 = self.g.vs[e.target]['pos']
                midPoint = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
                normalVector = QVector2D(p1.y() - p2.y(), p2.x() - p1.x())
                startVector = QVector2D(midPoint.x() - normalVector.x() / 2, midPoint.y() - normalVector.y() / 2)
                incVector = normalVector / (count - 1)
                multipleEdge[(e.source, e.target)] = [(p1, p2, (startVector + incVector * i).toPointF())
                                                      for i in range(count)]

        def createLine(e):
            result = multipleEdge.get((e.source, e.target))
            if result:
                p1, p2, controlPoint = result.pop()
                path = QPainterPath(p1)
                path.quadTo(controlPoint, p2)
                path.quadTo(controlPoint, p1)
                return path
            return QLineF(
                self.g.vs[e.source]['pos'],
                self.g.vs[e.target]['pos'],
            )

        self.g.es['line'] = [createLine(e) for e in self.g.es]

        self.pointsToDraw = [v for v in self.g.vs if self.viewRect.contains(v['x'], v['y'])]

        linesInScreen = {e for e in self.g.es if inScreen(e)}
        linesIntersectScreen = {e for e in self.g.es if intersectWithViewRect(e['line'])}
        self.linesToDraw = linesInScreen.union(linesIntersectScreen)

        # filter
        if self.filterData is not None:
            self.linesToDraw = list(filter(
                lambda e: self.filterData['left'] < e[self.filterData['attr']] < self.filterData['right'],
                self.linesToDraw
            ))

    def paintEvent(self, event):
        self.updateViewRect()
        painter = QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        try:
            if self.viewMode == GEO_MODE:
                painter.drawImage(self.SCREEN_RECT, self.backGroundImage, self.backgroundRect)
            else:
                painter.fillRect(self.SCREEN_RECT, QBrush(self.backgroundColor))

            for edge in self.linesToDraw:
                line = edge['line']
                painter.setPen(QPen(edge['color'], 1.3, join=Qt.PenJoinStyle(0x80)))
                if isinstance(line, QLineF):
                    painter.drawLine(line)
                else:
                    painter.drawPath(line)

            painter.setPen(QPen(self.backgroundColor, 0.5, join=Qt.PenJoinStyle(0x80)))

            for v in self.pointsToDraw:
                painter.setBrush(QBrush(v['color']))
                painter.drawEllipse(
                    int(v['pos'].x() - self.POINT_RADIUS / 2.0),
                    int(v['pos'].y() - self.POINT_RADIUS / 2.0),
                    self.POINT_RADIUS, self.POINT_RADIUS
                )

            painter.setPen(QPen(Qt.red, 4, join=Qt.PenJoinStyle(0x80)))

            for e in self.selectedLines:
                line = e['line']
                if isinstance(line, QLineF):
                    painter.drawLine(line)
                else:
                    painter.drawPath(line)

            for v in self.selectedPoints:
                painter.setBrush(v['color'])
                painter.drawEllipse(
                    int(v['pos'].x() - self.SELECTED_POINT_RADIUS / 2),
                    int(v['pos'].y() - self.SELECTED_POINT_RADIUS / 2),
                    self.SELECTED_POINT_RADIUS, self.SELECTED_POINT_RADIUS
                )
        except Exception as exception:
            print(exception)

    def findShortestPath(self):
        path = self.g.get_shortest_paths(self.selectedPoints[0], self.selectedPoints[1],
                                         self.shortestPathWeight, output='epath')
        if path[0]:
            self.selectedLines = [self.g.es[i] for i in path[0]]
            self.selectedPoints = [self.g.vs[e.source] for e in self.selectedLines] + [self.selectedPoints[1]]

    def findBottleNeck(self):
        clusterOutgoingEdges = {cl: [] for cl in set(self.g.vs['cluster'])}
        for e in self.g.es:
            targetCluster = self.g.vs[e.target]['cluster']
            sourceCluster = self.g.vs[e.source]['cluster']
            if targetCluster != sourceCluster:
                clusterOutgoingEdges[targetCluster].append(e)
                clusterOutgoingEdges[sourceCluster].append(e)
        self.selectedLines = []
        self.selectedPoints = []
        for cluster, edges in clusterOutgoingEdges.items():
            if len(edges) == 1:
                e = edges[0]
                self.selectedLines.append(e)
                self.selectedPoints.append(self.g.vs[e.target])
                self.selectedPoints.append(self.g.vs[e.source])
        self.update()

    def startRealTime(self, randomInputs):
        # neu co thread cu, stop thread cu, tao thread moi
        # tao thread, luu thread vao self.updateThread
        # trong thread, while true -> tao random -> self.update -> sleep
        # remember to delete daemon
        vertexAttr = []
        edgeAttr = []
        fps = 3
        for randomInput in randomInputs:
            if randomInput[3] in self.g.vs.attributes():
                vertexAttr.append(randomInput)
            else:
                edgeAttr.append(randomInput)

        print("vertex's attribute ", vertexAttr)
        print("edge's attributes ", edgeAttr)
        thread = threading.Thread(target=self.doRealTime, args=(vertexAttr, edgeAttr, fps), daemon=True)
        self.threading = thread
        thread.start()

    def doRealTime(self, vertexAttr, edgeAttr, fps):
        while self.inRealTimeMode:
            if len(vertexAttr) > 0:
                for v in vertexAttr:
                    if v[0] == "Normal Distribution":
                        self.g.vs[v[3]] = [random.normal(v[1], v[2]) for i in range(self.g.vcount())]
                    else:
                        self.g.vs[v[3]] = [random.uniform(v[1], v[2]) for i in range(self.g.vcount())]

            if len(edgeAttr) > 0:
                for edge in edgeAttr:
                    if edge[0] == "Normal Distribution":
                        self.g.es[edge[3]] = [random.normal(edge[1], edge[2]) for i in range(self.g.ecount())]
                    else:
                        self.g.es[edge[3]] = [random.uniform(edge[1], edge[2]) for i in range(self.g.ecount())]
            self.setEdgeColor()
            time.sleep(1.0 / fps)
            self.update()

    def vertexDegree(self):
        self.g.vs['degree'] = 0
        for i in range(len(self.g.vs)):
            self.g.vs[i]['degree'] = self.g.vs[i].degree()

    def zoomInEvent(self):
        self.zoom *= 1.2
        self.update()

    def zoomOutEvent(self):
        self.zoom /= 1.2
        self.update()

    def zoomResetEvent(self):
        self.zoom = 1
        self.center = QPointF(self.WIDTH / 2, self.HEIGHT / 2)
        self.update()

    def wheelEvent(self, event):
        if self.backgroundDragging:
            return
        self.zoom += event.angleDelta().y() / 120 * 0.05
        self.update()

    def cancelFilter(self):
        self.filterData = None
        self.update()

    def selectPoint(self, v):
        if self.mode == self.MODE_EDIT:
            self.pointDragging = v
            self.selectedLines = []
            self.gui.displayVertex(v)

            if self.deleteNode:
                if v in self.selectedPoints:
                    self.selectedPoints.remove(v)
                self.selectedLines = filter(lambda e: v.index not in [e.source, e.target], self.selectedLines)
                self.g.delete_vertices(v)
                self.deleteNode = None

            if self.addLine:
                if len(self.selectedPoints) == 2:
                    self.selectedPoints = []
                self.selectedPoints.append(v)
                if len(self.selectedPoints) == 2:
                    self.g.add_edge(self.selectedPoints[0], self.selectedPoints[1])
                    self.selectedPoints = []
                    self.addLine = None
            self.selectedPoints = [v]

        elif self.mode == self.MODE_FIND_SHORTEST_PATH:
            spl = len(self.selectedPoints)
            if spl == 0 or spl >= 2:
                self.selectedPoints = [v]
                self.selectedLines = []
            else:
                self.selectedPoints.append(v)
                self.findShortestPath()

        elif self.mode == self.MODE_FIND_BOTTLE_NECK:
            self.pointDragging = v

    def selectLine(self, l):
        if self.mode == self.MODE_EDIT:
            self.selectedLines = [l]
            self.selectedPoints = []
            self.gui.displayEdge(l)

        if self.deleteLine:
            self.selectedLines.remove(l)
            self.g.delete_edges(l)
            self.deleteLine = None

    def mousePressEvent(self, event):
        pos = event.pos()

        clickedSquare = QPainterPath(pos)
        clickedSquare.addRect(QRectF(
            pos.x() - self.CURVE_SELECT_SQUARE_SIZE / 2,
            pos.y() - self.CURVE_SELECT_SQUARE_SIZE,
            self.CURVE_SELECT_SQUARE_SIZE,
            self.CURVE_SELECT_SQUARE_SIZE
        ))

        def clickToLine(line):
            if isinstance(line, QLineF):
                try:
                    d = abs((line.x2() - line.x1()) * (line.y1() - pos.y()) - (line.x1() - pos.x()) * (
                            line.y2() - line.y1())) / sqrt((line.x2() - line.x1()) ** 2 + (line.y2() - line.y1()) ** 2)
                except ZeroDivisionError:
                    return False
                return d < self.LINE_DISTANCE and min(line.x1(), line.x2()) < pos.x() < max(line.x1(), line.x2())

            return line.intersects(clickedSquare)

        def clickedToPoint(point):
            return self.POINT_RADIUS ** 2 >= (point.x() - pos.x()) ** 2 + (point.y() - pos.y()) ** 2

        for v in self.pointsToDraw:
            if clickedToPoint(v['pos']):
                self.selectPoint(v)
                self.update()
                return
        for l in self.linesToDraw:
            if clickToLine(l['line']):
                self.selectLine(l)
                self.update()
                return

        if self.mode == self.MODE_EDIT:
            self.selectedPoints = []
            self.selectedLines = []

            if self.addNode:
                coordinate = {
                    'x': float(pos.x() / self.zoom + self.viewRect.x()),
                    'y': float(pos.y() / self.zoom + self.viewRect.y()),
                    'cluster': 0,
                    'color': Qt.white,
                    'pos': pos,
                }
                self.g.add_vertex(name=None, **coordinate)
                self.addNode = None
                self.update()

        self.backgroundDragging = pos
        self.update()

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.backgroundDragging is not None:
            self.center = QPointF(
                self.center.x() + (self.backgroundDragging.x() - pos.x()) / self.zoom,
                self.center.y() + (self.backgroundDragging.y() - pos.y()) / self.zoom,
            )
            self.backgroundDragging = pos
            self.update()
        elif self.pointDragging is not None:
            self.pointDragging['x'] = pos.x() / self.zoom + self.viewRect.x()
            self.pointDragging['y'] = pos.y() / self.zoom + self.viewRect.y()
            self.update()

    def mouseReleaseEvent(self, event):
        self.backgroundDragging = self.pointDragging = None
