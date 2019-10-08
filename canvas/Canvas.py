from math import sqrt
from typing import Union

import igraph
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from igraph import Graph
from numpy import *

from .Mode import Mode
from .utils import *


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

    DEFAULT_CLUSTERING_ALGO = 'community_edge_betweenness'
    DEFAULT_GRAPH_LAYOUT = 'layout_circle'

    def __init__(self, width: int, height: int):
        super().__init__(None)

        self.WIDTH = width
        self.HEIGHT = height
        self.SCREEN_RECT = QRectF(0, 0, width, height)
        self.SCREEN_RECT_LINE = [
            QLineF(0, 0, width, 0),
            QLineF(width, 0, width, height),
            QLineF(width, height, 0, height),
            QLineF(0, height, 0, 0)
        ]

        self.center = self.zoom = None
        self.backgroundDragging = None
        self.selectedEdges = self.selectedVertices = []
        self.viewRect = self.verticesToDraw = self.edgesToDraw = None

        self.modes = []
        self.g = None

    def toScaledXY(self, x, y):
        return self.toScaledX(x), self.toScaledY(y)

    def toScaledX(self, x):
        return float((x - self.viewRect.x()) * self.zoom)

    def toScaledY(self, y):
        return float((y - self.viewRect.y()) * self.zoom)

    def toAbsoluteXY(self, x, y):
        return self.toAbsoluteX(x), self.toAbsoluteY(y)

    def toAbsoluteX(self, x):
        return float(x / self.zoom + self.viewRect.x())

    def toAbsoluteY(self, y):
        return float(y / self.zoom + self.viewRect.y())

    def setGraph(self, g: Union[str, Graph]):
        if isinstance(g, str):
            g = igraph.read(g)
        self.g = g
        g.vs['degree'] = [v.degree() for v in g.vs]
        for mode in self.modes:
            if mode.onSetGraph():
                break
        self.notifyGraphUpdated()
        self.resetViewRect()
        self.update()

    def notifyGraphUpdated(self):
        for mode in self.modes:
            if mode.onUpdateGraph():
                break

    def addMode(self, mode: Mode):
        if mode in self.modes:
            mode.onUnset()
            mode.onSet()
            self.update()
            return

        def isConflict(m: Mode):
            if m.__class__.__name__ in mode.conflict_modes:
                return True
            return False

        mode.canvas = self
        mode.onSet()
        self.modes = [m for m in self.modes if not isConflict(m)]
        self.modes = sorted(self.modes + [mode], key=lambda m: m.priority)
        self.update()

    def removeMode(self, mode: Mode):
        if mode in self.modes:
            self.modes.remove(mode)
            mode.onUnset()
            return True
        return False

    def resetViewRect(self):
        for mode in self.modes:
            if mode.onResetViewRect():
                break

        self.center = QPointF(self.WIDTH / 2, self.HEIGHT / 2)
        self.zoom = 1
        self.backgroundDragging = None
        self.selectedEdges = self.selectedVertices = []

        self.updateViewRect()

    def updateViewRect(self):
        viewRectWidth = self.WIDTH / self.zoom
        viewRectHeight = self.HEIGHT / self.zoom
        viewRectX = self.center.x() - viewRectWidth / 2
        viewRectY = self.center.y() - viewRectHeight / 2
        self.viewRect = QRectF(viewRectX, viewRectY, viewRectWidth, viewRectHeight)

        def intersectWithViewRect(line):
            if isinstance(line, QLineF):
                return any([line.intersect(vrl, QPointF()) == 1 for vrl in self.SCREEN_RECT_LINE])
            return line.intersects(self.SCREEN_RECT)

        def inScreen(edge):
            return self.SCREEN_RECT.contains(self.g.vs[edge.source]['pos']) \
                   or self.SCREEN_RECT.contains(self.g.vs[edge.target]['pos'])

        self.g.vs['pos'] = [QPointF(
            self.toScaledX(v['x']),
            self.toScaledY(v['y'])
        ) for v in self.g.vs]

        multipleEdge = {}
        for e in self.g.es:
            count = e.count_multiple()
            key = (e.source, e.target)
            if count > 1 and key not in multipleEdge:
                p1 = self.g.vs[e.source]['pos']
                p2 = self.g.vs[e.target]['pos']
                midPoint = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
                normalVector = QVector2D(p1.y() - p2.y(), p2.x() - p1.x())
                startVector = QVector2D(midPoint.x() - normalVector.x() / 2, midPoint.y() - normalVector.y() / 2)
                incVector = normalVector / (count - 1)
                multipleEdge[key] = [(p1, p2, (startVector + incVector * i).toPointF())
                                     for i in range(count)]

        def createLine(edge):
            result = multipleEdge.get((edge.source, edge.target))
            if result:
                pos1, pos2, controlPoint = result.pop()
                path = QPainterPath(pos1)
                path.quadTo(controlPoint, pos2)
                path.quadTo(controlPoint, pos1)
                return path
            return QLineF(
                self.g.vs[edge.source]['pos'],
                self.g.vs[edge.target]['pos'],
            )

        self.g.es['line'] = [createLine(e) for e in self.g.es]

        self.verticesToDraw = [v for v in self.g.vs if self.viewRect.contains(v['x'], v['y'])]

        linesInScreen = {e for e in self.g.es if inScreen(e)}
        linesIntersectScreen = {e for e in self.g.es if intersectWithViewRect(e['line'])}
        self.edgesToDraw = list(linesInScreen.union(linesIntersectScreen))

        for mode in self.modes:
            if mode.onUpdateViewRect():
                break

    def paintEvent(self, event):
        self.updateViewRect()
        painter = QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        for mode in self.modes:
            if mode.onPaintBegin(painter):
                break

        for mode in self.modes:
            if mode.beforePaintEdges(painter):
                break
        for edge in self.edgesToDraw:
            painter.setPen(edge['color'])
            line = edge['line']
            if isinstance(line, QLineF):
                painter.drawLine(line)
            else:
                painter.drawPath(line)

        for mode in self.modes:
            if mode.beforePaintVertices(painter):
                break
        for vertex in self.verticesToDraw:
            painter.setBrush(vertex['color'])
            painter.drawEllipse(
                int(vertex['pos'].x() - self.POINT_RADIUS / 2.0),
                int(vertex['pos'].y() - self.POINT_RADIUS / 2.0),
                self.POINT_RADIUS, self.POINT_RADIUS
            )

        for mode in self.modes:
            if mode.beforePaintSelectedEdges(painter):
                break
        for edge in self.selectedEdges:
            line = edge['line']
            if isinstance(line, QLineF):
                painter.drawLine(line)
            else:
                painter.drawPath(line)

        for mode in self.modes:
            if mode.beforePaintSelectedVertices(painter):
                break
        for vertex in self.selectedVertices:
            painter.setBrush(vertex['color'])
            painter.drawEllipse(
                int(vertex['pos'].x() - self.POINT_RADIUS / 2.0),
                int(vertex['pos'].y() - self.POINT_RADIUS / 2.0),
                self.POINT_RADIUS, self.POINT_RADIUS
            )

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
        self.zoom += event.angleDelta().y() / 120 * 0.05
        self.update()

    def mousePressEvent(self, event):
        pos = event.pos()

        clickedSquare = QPainterPath(pos)
        clickedSquare.addRect(QRectF(
            pos.x() - self.CURVE_SELECT_SQUARE_SIZE / 2,
            pos.y() - self.CURVE_SELECT_SQUARE_SIZE / 2,
            self.CURVE_SELECT_SQUARE_SIZE,
            self.CURVE_SELECT_SQUARE_SIZE
        ))

        def clickToLine(line):
            if isinstance(line, QLineF):
                try:
                    d = abs((line.x2() - line.x1()) * (line.y1() - pos.y()) - (line.x1() - pos.x()) *
                            (line.y2() - line.y1())) / sqrt((line.x2() - line.x1()) ** 2 + (line.y2() - line.y1()) ** 2)
                except ZeroDivisionError:
                    return False
                return d < self.LINE_DISTANCE and min(line.x1(), line.x2()) < pos.x() < max(line.x1(), line.x2())

            return line.intersects(clickedSquare)

        def clickedToPoint(point):
            return self.POINT_RADIUS ** 2 >= (point.x() - pos.x()) ** 2 + (point.y() - pos.y()) ** 2

        for v in self.verticesToDraw:
            if clickedToPoint(v['pos']):
                for mode in self.modes:
                    if mode.onSelectVertex(v):
                        break
                self.update()
                return

        for e in self.edgesToDraw:
            if clickToLine(e['line']):
                for mode in self.modes:
                    if mode.onSelectEdge(e):
                        break
                self.update()
                return

        for mode in self.modes:
            if mode.onSelectBackground(pos):
                return

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
        else:
            for mode in self.modes:
                if mode.onMouseMove(pos):
                    break
        self.update()

    def mouseReleaseEvent(self, event):
        self.backgroundDragging = None
        for mode in self.modes:
            if mode.onMouseRelease(event.pos()):
                return
