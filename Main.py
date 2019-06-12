import numpy as np
import matplotlib.pyplot as plt
import sys, os

sys.path.append("/home/felipe/SINMEC2018/PythonTools/Felipe/CgnsFile")
from CgnsFile import CgnsFile

sys.path.append("Grid/")
from Vertex import Vertex
from Element import Element

def main():
    cgnsFile = CgnsFile("/home/felipe/Downloads/12v_6x_2y.cgns")

    X = cgnsFile.coordinateX
    Y = cgnsFile.coordinateY
    nX = X.shape[1]
    nY = X.shape[0]
    cells = np.zeros((nY-1, nX-1), dtype=int)

    K = 1.0
    C = 1.0

    for j in range(0, nY-1):
        for i in range(0, nX-1):
            cells[j][i] = j*nX + i

    ###########################

    vertices = []
    for j in range(0, nY):
        for i in range(0, nX):
            vertices.append(Vertex(X[j][i], Y[j][i], j*nX + i))

    elements = []
    for j in range(0, nY - 1):
        for i in range(0, nX - 1):
            elements.append(Element(X[j][i], X[j][i+1], Y[j][i], Y[j+1][i], j*nX + i))

    ###########################

    west = np.zeros(nX)
    for i in range(1, nX):
        west[i] = X[0][i] - X[0][i-1]
    west[0] = 0.5 * (X[0][1] - X[0][0])

    east = np.zeros(nX)
    for i in range(0, nX-1):
        east[i] = X[0][i+1] - X[0][i]
    east[-1] = 0.5 * (X[0][-1] - X[0][-2])


    ###########################

    A = np.zeros(((nX-1) * (nY-1), (nX-1) * (nY-1)))

    for j in range(0, nY - 1):
        for i in range(1, nX - 2):
            A[cells[j][i]][cells[j][i-1]] = -1.0 * K / (C * west[i])
            A[cells[j][i]][cells[j][i]]   = K / (C * west[i]) + K / (C * east[i])
            A[cells[j][i]][cells[j][i+1]] = -1.0 * K / (C * east[i])

    for j in range(0, nY - 1):
        A[cells[j][0]][cells[j][0]] = K / (C * west[0]) + K / (C * east[0])
        A[cells[j][0]][cells[j][1]] = -1.0 * K / (C * east[0])

    for j in range(0, nY - 1):
        A[cells[j][-1]][cells[j][-2]] = -1.0 * K / (C * west[-1])
        A[cells[j][-1]][cells[j][-1]] = K / (C * west[-1]) + K / (C * east[-1])

    b = np.zeros((nX-1) * (nY-1))
    b[0] = 20.0 * K / (C * west[0])
    b[-1] = 100.0 *  K / (C * east[-1])

    t = np.linalg.solve(A, b)

    x = np.zeros((nX-1) * (nY-1))
    for i in range(0, nX - 1):
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

    # print("\n\tvertices")
    # for vertex in vertices:
    #     vertex.print()

    # print("\n\telements")
    # for element in elements:
    #     element.print()

    print("\n\tX - %i" % nX)
    for i in range(0, nX):
        print("\t\t%.5f" % X[0][i])

    print("\n\tY - %i" % nY)
    for j in range(0, nY):
        print("\t\t%.5f" % Y[j][0])

    print("\n\tcells")
    for j in range(0, nY-1):
        print("\t\t", end="")
        for i in range(0, nX-1):
            print("%2i " % (j*nX + i), end="")
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
