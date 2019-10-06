from threading import Thread
from time import sleep

from numpy import random

from .Mode import Mode


class RealTimeMode(Mode):
    priority = 4

    def __init__(self, gui):
        super().__init__(gui)
        self.vertexAttr = None
        self.edgeAttr = None
        self.fps = None
        self.inRealtimeMode = None
        self.thread = None

    def onSet(self):
        self.inRealtimeMode = True
        self.thread = Thread(target=self.doRealTime, daemon=True)
        self.thread.start()

    def onUnset(self):
        self.inRealtimeMode = False
        self.thread.join()

    def doRealTime(self):
        g = self.canvas.g
        while self.inRealtimeMode:
            if len(self.vertexAttr) > 0:
                for v in self.vertexAttr:
                    if v[0] == "Normal Distribution":
                        g.vs[v[3]] = random.normal(v[1], v[2], g.vcount())
                    else:
                        g.vs[v[3]] = random.uniform(v[1], v[2], g.vcount())

            if len(self.edgeAttr) > 0:
                for edge in self.edgeAttr:
                    if edge[0] == "Normal Distribution":
                        g.es[edge[3]] = random.normal(edge[1], edge[2], g.ecount())
                    else:
                        g.es[edge[3]] = random.uniform(edge[1], edge[2], g.ecount())

            self.canvas.notifyGraphUpdated()
            self.canvas.update()
            sleep(1.0 / self.fps)
