import numpy as np
import matplotlib.pyplot as plt
import sys, os

sys.path.append("/home/felipe/SINMEC2018/PythonTools/Felipe/CgnsFile")
from CgnsFile import CgnsFile

def main():
    cgnsFile = CgnsFile("/home/felipe/Downloads/12v_6x_2y.cgns")

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
            cells[j][i] = j*NVertexI + i

    ###########################

    west = np.zeros(NVertexI)
    for i in range(1, NVertexI):
        west[i] = X[0][i] - X[0][i-1]
    west[0] = 0.5 * (X[0][1] - X[0][0])

    east = np.zeros(NVertexI)
    for i in range(0, NVertexI-1):
        east[i] = X[0][i+1] - X[0][i]
    east[-1] = 0.5 * (X[0][-1] - X[0][-2])

    ###########################

    A = np.zeros((NCellI * NCellJ, NCellI * NCellJ))

    for j in range(0, NCellJ):
        for i in range(1, NCellI - 1):
            A[cells[j][i]][cells[j][i-1]] = -1.0 * K / (C * west[i])
            A[cells[j][i]][cells[j][i]]   = K / (C * west[i]) + K / (C * east[i])
            A[cells[j][i]][cells[j][i+1]] = -1.0 * K / (C * east[i])

    for j in range(0, NCellJ):
        A[cells[j][0]][cells[j][0]] = K / (C * west[0]) + K / (C * east[0])
        A[cells[j][0]][cells[j][1]] = -1.0 * K / (C * east[0])

    for j in range(0, NCellJ):
        A[cells[j][-1]][cells[j][-2]] = -1.0 * K / (C * west[-1])
        A[cells[j][-1]][cells[j][-1]] = K / (C * west[-1]) + K / (C * east[-1])

    b = np.zeros(NCellI * NCellJ)
    b[0] = 20.0 * K / (C * west[0])
    b[-1] = 100.0 *  K / (C * east[-1])

    t = np.linalg.solve(A, b)

    x = np.zeros(NCellI * NCellJ)
    for i in range(0, NCellI):
        x[i] = 0.5 * (X[0][i+1] + X[0][i])

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
            print("%2i " % (j*NVertexI + i), end="")
    print()

    print("\n\tw")
    for w in west:
        print("\t\t%.5f" % w)

    print("\n\te")
    for e in east:
        print("\t\t%.5f" % e)

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
