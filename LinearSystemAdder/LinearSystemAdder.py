import numpy as np

class LinearSystemAdder(object):
    def __init__(self, cells, deltas, matrix, independent):

        self.cells = cells
        self.matrix = matrix
        self.independent = independent

        self.NCellI = cells.shape[1]
        self.NCellJ = cells.shape[0]

        self.west = deltas["west"]
        self.east = deltas["east"]
        self.south = deltas["south"]
        self.north = deltas["north"]

    def addToLinearSystem(self):
        self.addToMatrix()
        self.addToIndepedent()

    def addToMatrix(self):
        pass

    def addToIndependent(self):
        pass
