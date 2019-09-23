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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.g = g = igraph.read('resource/graph/NREN-delay.graphml')
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
        self.backgroundDragging = self.pointDragging = None
        self.center = QPointF(size.width() / 2, size.height() / 2)
        self.zoom = 1
        self.viewRect = self.toDraw = None
        self.updateViewRect()

    def updateViewRect(self):
        size = self.size()
        viewRectWidth = size.width() / self.zoom
        viewRectHeight = size.height() / self.zoom
        viewRectX = self.center.x() - viewRectWidth / 2
        viewRectY = self.center.y() - viewRectHeight / 2
        self.viewRect = QRectF(viewRectX, viewRectY, viewRectWidth, viewRectHeight)

        self.g.vs['pos'] = [QPointF(
            (v['x'] - viewRectX) * self.zoom,
            (v['y'] - viewRectY) * self.zoom
        ) for v in self.g.vs]

        self.toDraw = [v for v in self.g.vs if self.viewRect.contains(v['x'], v['y'])]

    def paintEvent(self, event):
        self.updateViewRect()

        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(Qt.black))

        painter.setPen(QPen(Qt.white, 0.5, join=Qt.PenJoinStyle(0x80)))
        for e in self.g.es:
            painter.drawLine(
                self.g.vs[e.source]['pos'],
                self.g.vs[e.target]['pos'],
            )

        painter.setPen(QPen(Qt.black, 1))
        for v in self.toDraw:
            painter.setBrush(self.asnToColor[v['asn']])
            painter.drawEllipse(
                v['pos'].x() - self.POINT_RADIUS / 2,
                v['pos'].y() - self.POINT_RADIUS / 2,
                self.POINT_RADIUS, self.POINT_RADIUS
            )

        painter.end()

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

        def clickedToPoint(point):
            return self.POINT_RADIUS ** 2 >= (point.x() - pos.x()) ** 2 + (point.y() - pos.y()) ** 2

        for v in self.toDraw:
            if clickedToPoint(v['pos']):
                self.pointDragging = v
                print(v['id'])
                return

        self.backgroundDragging = pos

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
