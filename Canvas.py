from math import sqrt
from random import choice

import igraph
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def randomColor():
    return QBrush(QColor(choice(range(0, 256)), choice(range(0, 256)), choice(range(0, 256))))


class Canvas(QWidget):
    HEIGHT = 400
    POINT_RADIUS = 8
    LINE_DISTANCE = 2

    def __init__(self, gui, fileName="resource/graph/NREN-delay.graphml"):
        super().__init__(None)
        self.defaultUrl = 'resource/graph/NREN-delay.graphml'
        self.gui = gui

        self.g = self.asnToColor = None
        self.setGraph('resource/graph/NREN-delay.graphml')

    def setGraph(self, url):
        self.g = g = igraph.read(url)


        self.asnToColor = {asn: randomColor() for asn in set(g.vs['asn'])}

        # use translation to convert negative coordinates to non-negative
        mx = min(g.vs['x'])
        my = min(g.vs['y'])
        g.vs['x'] = [x - mx for x in g.vs['x']]
        g.vs['y'] = [y - my for y in g.vs['y']]

        mx = max(g.vs['x'])
        my = max(g.vs['y'])
        self.ratio = mx / my
        size = self.sizeHint()

        # convert init coordinates to coordinates on window
        g.vs['x'] = [x / mx * size.width() for x in g.vs['x']]
        g.vs['y'] = [y / my * size.height() for y in g.vs['y']]

        # Init
        self.backgroundDragging = self.pointDragging = self.selectedLine = self.selectedPoint = None
        self.center = QPointF(size.width() / 2, size.height() / 2)
        self.zoom = 1
        self.viewRect = self.pointsToDraw = self.linesToDraw = None
        self.updateViewRect()

    def updateViewRect(self):
        size = self.size()
        w = size.width()
        h = size.height()
        viewRectWidth = w / self.zoom
        viewRectHeight = h / self.zoom
        viewRectX = self.center.x() - viewRectWidth / 2
        viewRectY = self.center.y() - viewRectHeight / 2
        self.viewRect = QRectF(viewRectX, viewRectY, viewRectWidth, viewRectHeight)

        viewRectLines = [
            QLineF(0, 0, w, 0),
            QLineF(w, 0, w, h),
            QLineF(w, h, 0, h),
            QLineF(0, h, 0, 0)
        ]

        def intersectWithViewRect(line):
            return any([line.intersect(vrl, QPointF()) == 1 for vrl in viewRectLines])

        screenRect = QRectF(0, 0, w, h)

        def inScreen(edge):
            return screenRect.contains(self.g.vs[edge.source]['pos']) or screenRect.contains(
                self.g.vs[edge.target]['pos'])

        self.g.vs['pos'] = [QPointF(
            (v['x'] - viewRectX) * self.zoom,
            (v['y'] - viewRectY) * self.zoom
        ) for v in self.g.vs]

        self.g.es['line'] = [QLineF(
            self.g.vs[e.source]['pos'],
            self.g.vs[e.target]['pos'],
        ) for e in self.g.es]

        self.pointsToDraw = [v for v in self.g.vs if self.viewRect.contains(v['x'], v['y'])]

        linesInScreen = {e for e in self.g.es if inScreen(e)}
        linesIntersectScreen = {e for e in self.g.es if intersectWithViewRect(e['line'])}
        self.linesToDraw = linesInScreen.union(linesIntersectScreen)

    def paintEvent(self, event):
        self.updateViewRect()

        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(Qt.black))
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        for e in self.linesToDraw:
            if e == self.selectedLine:
                painter.setPen(QPen(Qt.red, 2, join=Qt.PenJoinStyle(0x80)))
            else:
                painter.setPen(QPen(Qt.white, 0.5, join=Qt.PenJoinStyle(0x80)))
            painter.drawLine(e['line'])

        for v in self.pointsToDraw:
            if v == self.selectedPoint:
                painter.setPen(QPen(Qt.red, 3))
            else:
                painter.setPen(QPen(Qt.black, 1))
            painter.setBrush(self.asnToColor[v['asn']])
            painter.drawEllipse(
                v['pos'].x() - self.POINT_RADIUS / 2,
                v['pos'].y() - self.POINT_RADIUS / 2,
                self.POINT_RADIUS, self.POINT_RADIUS
            )

    def zoomInEvent(self):
        self.zoom += 0.2
        self.update()

    def zoomOutEvent(self):
        self.zoom -= 0.2
        self.update()

    def zoomResetEvent(self):
        self.zoom = 1
        self.update()

    def wheelEvent(self, event):
        if self.backgroundDragging:
            return
        self.zoom += event.angleDelta().y() / 120 * 0.05
        self.update()

    def mousePressEvent(self, event):
        pos = event.pos()

        def clickToLine(line):
            try:
                d = abs((line.x2() - line.x1()) * (line.y1() - pos.y()) - (line.x1() - pos.x()) * (
                        line.y2() - line.y1())) / sqrt((line.x2() - line.x1()) ** 2 + (line.y2() - line.y1()) ** 2)
            except ZeroDivisionError:
                return False
            return d < self.LINE_DISTANCE and min(line.x1(), line.x2()) < pos.x() < max(line.x1(), line.x2())

        def clickedToPoint(point):
            return self.POINT_RADIUS ** 2 >= (point.x() - pos.x()) ** 2 + (point.y() - pos.y()) ** 2

        # Ongoing
        for l in self.linesToDraw:
            if clickToLine(l['line']):
                self.selectedLine = l
                self.gui.displayVertex(l['weight'])
                self.selectedPoint = None
                # self.gui.displayLine(l)
                self.update()
                print(l)
                return

        for v in self.pointsToDraw:
            if clickedToPoint(v['pos']):
                self.pointDragging = v
                # self.gui.displayVertex(v)
                self.selectedPoint = v
                self.selectedLine = None
                self.update()
                return

        self.backgroundDragging = pos
        self.selectedPoint = None
        self.selectedLine = None
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

    def sizeHint(self):
        return QSize(self.HEIGHT * self.ratio, self.HEIGHT)
