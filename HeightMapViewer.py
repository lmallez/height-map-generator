#!/usr/bin/python3

from deprecated_files import HeightMapGenerator
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import sys

def displayMap(map):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    N = len(map)
    X, Y = np.meshgrid(np.arange(N), np.arange(N))
    Z = np.array(map)
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    plt.show()


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    displayMap(HeightMapGenerator.genMap(arg))
