import igraph as ig
class constraintAttr():
    attrEdge = {"total delay","link speed raw"}
    attrNode = {"latitude","longtitude"}
    def __init__(self,graph):
        self.g = graph
    def checkConstrainEdge(self):
        currAttr = self.g.es.attributes()
        for i in currAttr:
            if i.upper() in self.attrEdge:
                return True
        return False

    def checkConstrainVertex(self):
        currAttr = (self.g).vs.attributes()
        for i in currAttr:
            if i.upper() in self.attrNode:
                return True
        return False
    def check(self):
        while not self.checkConstrainEdge() and self.checkConstrainVertex()):
            return True
        self.notify()
        return False
    def link(self,missingAttr,linkAttr, type):
         if type.upper()=="EDGE":
             print("Edge")
         elif type.upper()=="VERTEX":
             print("Vertex")
    def notify(self):
        print("Missing requirement attributes. Please choose input method")