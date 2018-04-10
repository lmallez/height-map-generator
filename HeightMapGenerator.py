#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
import random as ran

coef = 1

def isValidPoint(map, x, y):
    if x < 0 or y < 0 or x >= len(map) or y >= len(map) or map[x][y] is None:
        return False
    return True


def calcPtn(map, ptnList, state):
    avg = []
    for ptn in ptnList:
        if isValidPoint(map, ptn[0], ptn[1]) is True:
            avg.append(map[ptn[1]][ptn[0]])
    c = round(ran.uniform(-coef * state, coef * state))
    return np.mean(avg) + c


def getPointDiamond(map, x, y, state):
    ptn_list = [[x - 1, y - 1], [x - 1, y + 1], [x + 1, y + 1], [x + 1, y + 1]]
    return round(calcPtn(map, ptn_list, state), 3)


def getPointSquare(map, x, y, state):
    ptn_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
    return round(calcPtn(map, ptn_list, state), 3)


def diamondMap(map, state):
    size = len(map)
    for y in range(0, size - 1):
        for x in range(0, size - 1):
            if map[x][y] is not None and map[x + 1][y + 1] is None:
                map[x + 1][y + 1] = getPointDiamond(map, x + 1, y + 1, state)
    return map

def squareMap(map, state):
    size = len(map)
    for y in range(0, size):
        for x in range(0, size):
            if map[x][y] is None:
                map[x][y] = getPointSquare(map, x, y, state)
    return map


def doubleMap(map):
    size = len(map)
    newMap = []
    for y in range(0, size):
        line1 = []
        line2 = []
        for x in range(0, size):
            line1.append(map[x][y])
            line2.append(None)
            if x < size - 1:
                line1.append(None)
                line2.append(None)
        newMap.append(line1)
        if y < size - 1:
            newMap.append(line2)
    return newMap


def increase(map, state):
    map = doubleMap(map)
    map = diamondMap(map, state)
    map = squareMap(map, state)
    return map


def printMap(a):
    for y in range(0, len(a)):
        tmp = list(map(int, a[y]))
        print(*tmp, sep=',')


def genMap(len):
    map = [[ran.uniform(0, 20), ran.uniform(0, 20)], [ran.uniform(0, 20), ran.uniform(0, 20)]]
    for i in range(0, len):
        map = increase(map, len - i)
    return map


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    printMap(genMap(arg))
