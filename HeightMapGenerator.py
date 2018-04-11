#!/usr/bin/python3

import sys
import numpy as np
import random as ran

coef = 3

def isValidPoint(map, x, y):
    if x < 0 or y < 0 or x >= len(map) or y >= len(map) or map[y][x] is None:
        return False
    return True


def calcPtn(map, ptnList, state):
    avg = []
    for ptn in ptnList:
        if isValidPoint(map, ptn[0], ptn[1]) is True:
            avg.append(map[ptn[1]][ptn[0]])
    c = ran.uniform(-coef * state, coef * state)
    return np.mean(avg) + c


def getPointDiamond(map, x, y, pad, coef):
    ptn_list = [[x - pad, y - pad], [x - pad, y + pad], [x + pad, y - pad], [x + pad, y + pad]]
    return round(calcPtn(map, ptn_list, pad), 3)


def getPointSquare(map, x, y, pad, coef):
    ptn_list = [[x, y - pad], [x, y + pad], [x - pad, y], [x + pad, y]]
    return round(calcPtn(map, ptn_list, pad), 3)


def diamondMap(map, pad, coef):
    size = int(len(map) / pad) - 1
    for y in range(0, size):
        for x in range(0, size):
            if map[y * pad][x * pad] is not None and map[y * pad + pad][x * pad + pad] is None:
                map[y * pad + pad][x * pad + pad] = getPointDiamond(map, x * pad + pad, y * pad + pad, pad, coef)
    return map


def squareMap(map, pad, coef):
    size = int(len(map) / pad)
    for y in range(0, size):
        for x in range(0, size):
            if map[y * pad][x * pad] is None:
                map[y * pad][x * pad] = getPointSquare(map, x * pad, y * pad, pad, coef)
    return map


def createMap(size):
    map = [[None for y in range(0, size)] for x in range(0, size)]
    return map

def setPointBoder(map):
    size = len(map)
    map[0][0] = ran.uniform(-coef * size, coef * size)
    map[0][size - 1] = ran.uniform(-coef * size, coef * size)
    map[size - 1][0] = ran.uniform(-coef * size, coef * size)
    map[size - 1][size - 1] = ran.uniform(-coef * size, coef * size)
    return map

def increase(map, pad, coef):
    map = diamondMap(map, pad, coef)
    map = squareMap(map, pad, coef)
    return map


def genMap(size):
    ran.seed()
    maxLarg = 2
    for i in range(0, size):
        maxLarg = maxLarg * 2 - 1
    map = createMap(maxLarg)
    map = setPointBoder(map)
    print("[Map %d x %d created]" % (maxLarg, maxLarg))
    pad = int((maxLarg - 1) / 2)
    for i in range(1, size + 1):
        map = increase(map, int(pad), 0.1)
        pad = int(pad / 2)
    return map

def printMap(a):
    for y in range(0, len(a)):
        tmp = list(map(int, a[y]))
        print(*tmp, sep=',')


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    #printMap(
    map = genMap(1)
    print(np.array(map))
