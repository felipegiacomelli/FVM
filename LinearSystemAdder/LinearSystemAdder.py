import numpy as np

class LinearSystemAdder(object):
    def __init__(self, cells, matrix, independent):

        self.cells = cells
        self.matrix = matrix
        self.independent = independent

    def addToLinearSystem(self):
        self.addToMatrix()
        self.addToIndepedent()

    def addToMatrix(self):
        pass

    def addToIndependent(self):
        pass
