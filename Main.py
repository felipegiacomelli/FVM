import numpy as np
import sys, os

sys.path.append("/home/felipe/SINMEC2018/PythonTools/Felipe/CgnsFile")
from CgnsFile import CgnsFile

def main():
    cgnsFile = CgnsFile("/home/felipe/Downloads/12v_4x_3y.cgns")

    X = cgnsFile.coordinateX
    Y = cgnsFile.coordinateY
    nX = X.shape[1]
    nY = X.shape[0]

    print()
    print("\tnX: %i" % nX)
    print("\tnY: %i" % nY)
    # print(X)
    # print(Y)

    print()
    for j in range(0, nY - 1):
        for i in range(0, nX - 1):
            print("\t%2i: %.5f, %.5f" % (j*nX + i, X[j][i+1] - X[j][i], Y[j+1][i] - Y[j][i]))

if __name__ == "__main__":
    main()
