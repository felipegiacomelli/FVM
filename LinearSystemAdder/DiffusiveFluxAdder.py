from LinearSystemAdder import LinearSystemAdder

K = 1.0
C = 1.0

class DiffusiveFluxAdder(LinearSystemAdder):
    def __init__(self, cells, deltas, matrix, independent):
        LinearSystemAdder.__init__(self, cells, deltas, matrix, independent)

    def addToMatrix(self):
        if self.NCellI > 1:
            for j in range(0, self.NCellJ):
                self.matrix[self.cells[j][0]][self.cells[j][0]] += K / (C * self.east[0])
                self.matrix[self.cells[j][0]][self.cells[j][1]] += -1.0 * K / (C * self.east[0])

                for i in range(1, self.NCellI - 1):
                    self.matrix[self.cells[j][i]][self.cells[j][i-1]] += -1.0 * K / (C * self.west[i])
                    self.matrix[self.cells[j][i]][self.cells[j][i]]   += K / (C * self.west[i]) + K / (C * self.east[i])
                    self.matrix[self.cells[j][i]][self.cells[j][i+1]] += -1.0 * K / (C * self.east[i])

                self.matrix[self.cells[j][-1]][self.cells[j][-2]] += -1.0 * K / (C * self.west[-1])
                self.matrix[self.cells[j][-1]][self.cells[j][-1]] += K / (C * self.west[-1])

            for j in range(0, self.NCellJ):
                self.matrix[self.cells[j][0]][self.cells[j][0]] += K / (C * self.west[0])
                self.independent[self.cells[j][0]] = 20.0 * K / (C * self.west[0])

            for j in range(0, self.NCellJ):
                self.matrix[self.cells[j][-1]][self.cells[j][-1]] += K / (C * self.east[-1])
                self.independent[self.cells[j][-1]] = 100.0 * K / (C * self.east[-1])

        if self.NCellJ > 1:
            for j in range(1, self.NCellJ - 1):
                self.matrix[self.cells[0][i]][self.cells[0][i]] += K / (C * self.north[0])
                self.matrix[self.cells[0][i]][self.cells[1][i]] += -1.0 * K / (C * self.north[0])

                for i in range(0, self.NCellI):
                    self.matrix[self.cells[j][i]][self.cells[j-1][i]] += -1.0 * K / (C * self.south[j])
                    self.matrix[self.cells[j][i]][self.cells[j][i]]   += K / (C * self.south[j]) + K / (C * self.north[j])
                    self.matrix[self.cells[j][i]][self.cells[j+1][i]] += -1.0 * K / (C * self.north[j])

                self.matrix[self.cells[-1][i]][self.cells[-2][i]] += -1.0 * K / (C * self.south[-1])
                self.matrix[self.cells[-1][i]][self.cells[-1][i]] += K / (C * self.south[-1])

            for i in range(0, self.NCellI):
                self.independent[self.cells[0][i]] += 0.0

            for i in range(0, self.NCellI):
                self.independent[self.cells[-1][i]] += 0.0

    def addToIndepedent(self):
        return
