import numpy as np
import matplotlib.pyplot as plt
import sys, os

sys.path.append("/home/felipe/SINMEC2018/Matplotlib/CgnsFile")
from CgnsFile import CgnsFile

sys.path.append("./LinearSystemAdder")
from DiffusiveFluxAdder import DiffusiveFluxAdder

def main():
    cgnsFile = CgnsFile("/home/felipe/Downloads/16v_4x_4y.cgns")

    X = cgnsFile.coordinateX
    Y = cgnsFile.coordinateY

    NVertexI = cgnsFile.zone.get(" data")[()][0][0]
    NVertexJ = cgnsFile.zone.get(" data")[()][0][1]
    NCellI = cgnsFile.zone.get(" data")[()][1][0]
    NCellJ = cgnsFile.zone.get(" data")[()][1][1]

    cells = np.zeros((NCellJ, NCellI), dtype=int)

    K = 1.0
    C = 1.0

    for j in range(0, NCellJ):
        for i in range(0, NCellI):
            cells[j][i] = j*NCellI + i

    print("\n\tX - %i" % NVertexI)
    for i in range(0, NVertexI):
        print("\t\t%.5f" % X[0][i])

    print("\n\tY - %i" % NVertexJ)
    for j in range(0, NVertexJ):
        print("\t\t%.5f" % Y[j][0])

    print("\n\tcells")
    for j in range(0, NCellJ):
        print("\t\t", end="")
        for i in range(0, NCellI):
            print("%2i " % cells[j][i], end="")
        print()

    ###########################
    deltas = {}

    west = np.zeros(NCellI)
    for i in range(1, NCellI):
        west[i] = X[0][i] - X[0][i-1]
    west[0] = 0.5 * (X[0][1] - X[0][0])
    deltas["west"] = west

    east = np.zeros(NCellI)
    for i in range(0, NCellI-1):
        east[i] = X[0][i+1] - X[0][i]
    east[-1] = 0.5 * (X[0][-1] - X[0][-2])
    deltas["east"] = east

    south = np.zeros(NCellJ)
    for j in range(1, NCellJ):
        south[j] = Y[j][0] - Y[j-1][0]
    south[0] = 0.5 * (Y[1][0] - Y[0][0])
    deltas["south"] = south

    north = np.zeros(NCellJ)
    for j in range(0, NCellJ-1):
        north[j] = Y[j+1][0] - Y[j][0]
    north[-1] = 0.5 * (Y[-1][0] - Y[-2][0])
    deltas["north"] = north

    ###########################

    A = np.zeros((NCellI * NCellJ, NCellI * NCellJ))
    b = np.zeros(NCellI * NCellJ)

    diffusiveFluxAdder = DiffusiveFluxAdder(cells, deltas, A, b)
    diffusiveFluxAdder.addToMatrix()

    # if NCellI > 1:
    #     for j in range(0, NCellJ):
    #         A[cells[j][0]][cells[j][0]] += K / (C * east[0])
    #         A[cells[j][0]][cells[j][1]] += -1.0 * K / (C * east[0])

    #         for i in range(1, NCellI - 1):
    #             A[cells[j][i]][cells[j][i-1]] += -1.0 * K / (C * west[i])
    #             A[cells[j][i]][cells[j][i]]   += K / (C * west[i]) + K / (C * east[i])
    #             A[cells[j][i]][cells[j][i+1]] += -1.0 * K / (C * east[i])

    #         A[cells[j][-1]][cells[j][-2]] += -1.0 * K / (C * west[-1])
    #         A[cells[j][-1]][cells[j][-1]] += K / (C * west[-1])

    #     for j in range(0, NCellJ):
    #         A[cells[j][0]][cells[j][0]] += K / (C * west[0])
    #         b[cells[j][0]] = 20.0 * K / (C * west[0])

    #     for j in range(0, NCellJ):
    #         A[cells[j][-1]][cells[j][-1]] += K / (C * east[-1])
    #         b[cells[j][-1]] = 100.0 * K / (C * east[-1])

    # if NCellJ > 1:
    #     for j in range(1, NCellJ - 1):
    #         A[cells[0][i]][cells[0][i]] += K / (C * north[0])
    #         A[cells[0][i]][cells[1][i]] += -1.0 * K / (C * north[0])

    #         for i in range(0, NCellI):
    #             A[cells[j][i]][cells[j-1][i]] += -1.0 * K / (C * south[j])
    #             A[cells[j][i]][cells[j][i]]   += K / (C * south[j]) + K / (C * north[j])
    #             A[cells[j][i]][cells[j+1][i]] += -1.0 * K / (C * north[j])

    #         A[cells[-1][i]][cells[-2][i]] += -1.0 * K / (C * south[-1])
    #         A[cells[-1][i]][cells[-1][i]] += K / (C * south[-1])

    #     for i in range(0, NCellI):
    #         b[cells[0][i]] += 0.0

    #     for i in range(0, NCellI):
    #         b[cells[-1][i]] += 0.0

    t = np.linalg.solve(A, b)

    x = np.zeros(NCellI * NCellJ)
    for j in range(0, NCellJ):
        for i in range(0, NCellI):
            x[cells[j][i]] = 0.5 * (X[j][i+1] + X[j][i])

    T = 80.0*X[0] + 20.0

    ###########################

    plt.rc("text", usetex=True)
    plt.rc("font", family="cantarell", weight="bold", size=16)

    figure, ax = plt.subplots()

    ax.plot(x, t, "om", label="Numerical")
    ax.plot(X[0], T, "-k", label="Analytical")
    ax.grid(True)
    ax.legend()
    ax.set_xlabel("Position X [m]")
    ax.set_ylabel("Temperature [K]")

    plt.tight_layout()
    plt.show()

    ###########################

    print("\n\tw")
    for w in west:
        print("\t\t%.5f" % w)

    print("\n\te")
    for e in east:
        print("\t\t%.5f" % e)

    print("\n\ts")
    for s in south:
        print("\t\t%.5f" % s)

    print("\n\tn")
    for n in north:
        print("\t\t%.5f" % n)

    ###########################

    print("\n\tA - %ix%i\n" % (A.shape[0], A.shape[1]))
    print(A)

    print("\n\tb - %i\n" % b.shape[0])
    print(b)

    print("\n\tt - %i\n" % t.shape[0])
    print(t)

    print("\n\tx - %i\n" % x.shape[0])
    print(x)

if __name__ == "__main__":
    main()
    print()
