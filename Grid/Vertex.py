import numpy as np

class Vertex(object):
    def __init__(self, x, y,handle = 0):

        self.x = x
        self.y = y
        self.handle = handle

    def print(self):
        print("\t\t%2i: %.5f, %.5f" % (self.handle, self.x, self.y))
