import numpy as np

from Vertex import Vertex

class Element(object):
    def __init__(self, x0, x1, y0, y1, handle):

        self.deltaX = x1 - x0
        self.deltaY = y1 - y0

        self.centroid = Vertex(np.mean([x0, x1]), np.mean([y0, y1]), 0)

        self.handle = handle

    def print(self):
        print("\t\t%2i: %.5f, %.5f | %.5f, %.5f" % (self.handle, self.centroid.x, self.centroid.y, self.deltaX, self.deltaY))
