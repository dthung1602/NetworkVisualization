from abc import ABC
from math import radians, pi, log, tan, isnan

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QBrush, QPen, QImage, QColor

from .Mode import Mode


class ViewMode(Mode, ABC):
    priority = 0

    backgroundBrush = None
    backgroundPen = None
    foregroundBrush = None
    foregroundPen = None
    selectedPen = QPen(Qt.red, 2)

    def onSet(self):
        g = self.canvas.g
        if g:
            g.es['color'] = [self.foregroundPen] * g.ecount()
            g.vs['color'] = [self.foregroundBrush] * g.vcount()

    def onSetGraph(self):
        g = self.canvas.g
        if 'color' not in g.es.attributes():
            g.es['color'] = [self.foregroundPen] * g.ecount()
        override = False
        if 'color' in g.vs.attributes() and g.vcount() > 0 and isinstance(g.vs[0]['color'], str):
            g.vs['cluster'] = g.vs['color']
            g.vs['color'] = [QBrush(QColor(c)) for c in g.vs['color']]
            override = True
        if 'color' in g.es.attributes() and g.ecount() > 0 and isinstance(g.es[0]['color'], str):
            g.es['cluster'] = g.es['color']
            g.es['color'] = [QPen(QColor(c)) for c in g.es['color']]
            override = True
        if override:
            return True
        if 'cluster' not in g.vs.attributes():
            g.vs['color'] = [self.foregroundBrush] * g.vcount()

    def onUpdateGraph(self):
        for e in self.canvas.g.es:
            if not e['color']:
                e['color'] = self.foregroundPen
        for v in self.canvas.g.vs:
            if not v['color']:
                v['color'] = self.foregroundBrush

    def onPaintBegin(self, painter: QPainter):
        painter.fillRect(self.canvas.SCREEN_RECT, self.backgroundBrush)

    def beforePaintEdges(self, painter):
        painter.setPen(self.foregroundPen)

    def beforePaintVertices(self, painter):
        painter.setPen(self.backgroundPen)

    def beforePaintSelectedEdges(self, painter):
        painter.setPen(self.selectedPen)

    def onSelectEdge(self, edge):
        return

    def onSelectVertex(self, vertex):
        return


class DarkViewMode(ViewMode):
    conflict_modes = ['LightViewMode', 'GeoViewMode']
    backgroundBrush = QBrush(Qt.black)
    backgroundPen = QPen(Qt.black)
    foregroundBrush = QBrush(Qt.darkGreen)
    foregroundPen = QPen(Qt.white)


class LightViewMode(ViewMode):
    conflict_modes = ['DarkViewMode', 'GeoViewMode']
    backgroundBrush = QBrush(Qt.white)
    backgroundPen = QPen(Qt.white)
    foregroundBrush = QBrush(Qt.darkBlue)
    foregroundPen = QPen(Qt.black)


class GeoViewMode(ViewMode):
    conflict_modes = ['LightViewMode', 'DarkViewMode']
    backgroundPen = QPen(Qt.black)
    foregroundPen = QPen(Qt.black)
    foregroundBrush = QBrush(Qt.darkBlue)

    def __init__(self, gui):
        super().__init__(gui)
        self.backGroundImage = QImage('resource/gui/maptovl.png')
        self.backgroundRect = None

    def geolocationToXY(self, longitude, latitude):
        x = (longitude + 180) * (self.canvas.WIDTH / 360)
        latRad = radians(latitude)
        mercN = log(tan((pi / 4) + (latRad / 2)))
        y = (self.canvas.HEIGHT / 2) - (self.canvas.WIDTH * mercN / (2 * pi))
        return x, y

    def onResetViewRect(self):
        for v in self.canvas.g.vs:
            longitude = v['Longitude']
            latitude = v['Latitude']
            if isnan(longitude) or isnan(latitude):
                v['x'] = self.canvas.WIDTH / 2
                v['y'] = self.canvas.HEIGHT / 2 + 150
            else:
                x, y = self.geolocationToXY(longitude, latitude)
                v['x'] = x
                v['y'] = y + 150
        return True

    def onUpdateViewRect(self):
        scale = self.backGroundImage.width() / self.canvas.WIDTH
        self.backgroundRect = QRectF(
            self.canvas.viewRect.x() * scale,
            self.canvas.viewRect.y() * scale,
            self.canvas.viewRect.width() * scale,
            self.canvas.viewRect.height() * scale
        )

    def onPaintBegin(self, painter: QPainter):
        painter.drawImage(
            self.canvas.SCREEN_RECT,
            self.backGroundImage,
            self.backgroundRect
        )
