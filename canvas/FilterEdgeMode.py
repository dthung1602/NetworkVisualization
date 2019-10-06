from .Mode import Mode


class FilterEdgeMode(Mode):
    priority = 3

    def __init__(self, gui):
        super().__init__(gui)
        self.attr = None
        self.left = None
        self.right = None

    def onUpdateViewRect(self):
        if self.attr is not None:
            self.canvas.edgesToDraw = list(filter(
                lambda e: self.left < e[self.attr] < self.right,
                self.canvas.edgesToDraw
            ))

    def setFilters(self, attr=None, left=float('-inf'), right=float('inf')):
        self.attr = attr
        self.left = left
        self.right = right
