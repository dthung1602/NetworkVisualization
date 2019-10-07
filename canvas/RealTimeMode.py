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
                        g.vs[v[2]] = [abs(random.normal(i, v[1])) for i in g.vs[v[2]]]
                    else:
                        g.vs[v[2]] = [abs(random.uniform(i - v[1], i + v[1])) for i in g.vs[v[2]]]

            if len(self.edgeAttr) > 0:
                for edge in self.edgeAttr:
                    if edge[0] == "Normal Distribution":
                        g.es[edge[2]] = [abs(random.normal(i, edge[1])) for i in g.es[edge[2]]]
                    else:
                        g.es[edge[2]] = [abs(random.uniform(i - edge[1], i + edge[1])) for i in g.es[edge[2]]]

            self.canvas.notifyGraphUpdated()
            self.canvas.update()
            sleep(1.0 / self.fps)
