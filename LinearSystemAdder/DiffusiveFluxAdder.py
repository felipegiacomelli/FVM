from LinearSystemAdder import LinearSystemAdder

class DiffusiveFluxAdder(LinearSystemAdder):
    def __init__(self, cells, A, b):
        LinearSystemAdder.__init__(self, cells, A, b)

    def addToMatrix(self):
        pass

    def addToIndepedent(self):
        pass
