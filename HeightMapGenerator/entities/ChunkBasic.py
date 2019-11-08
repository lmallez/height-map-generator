#!/bin/python3

import random as ran
from typing import List, Union

import numpy as np
from HeightMapGenerator.entities.Chunk import Chunk
from HeightMapGenerator.entities.Point import Point


class ChunkBasic(Chunk):
    def __init__(self, size, pos=Point(0, 0), coef=1):
        self.size = 2
        for i in range(0, size):
            self.size = self.size * 2 - 1
        self.init_map()
        self.set_border(coef)
        self.pos = pos

    def init_map(self):
        self.map: List[List[Union[int, None]]] = [[None for _ in range(0, self.size)] for _ in range(0, self.size)]

    @staticmethod
    def random_in(coef, avg):
        return ran.uniform(-coef / 2 + avg, coef / 2 + avg)

    def set_border_one(self, x, y, coef, avg=0):
        if self.map[y][x] is None:
            self.map[y][x] = self.random_in(coef, avg)

    def set_border(self, coef, avg=0):
        self.set_border_one(0, 0, coef, avg)
        self.set_border_one(self.size - 1, 0, coef, avg)
        self.set_border_one(0, self.size - 1, coef, avg)
        self.set_border_one(self.size - 1, self.size - 1, coef, avg)

    def at(self, x, y):
        if y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[y]):
            return None
        return self.map[y][x]

    @staticmethod
    def get_border(x, y):
        return [Point(x - 1, y),
                Point(x, y - 1),
                Point(x + 1, y),
                Point(x, y + 1)]

    def smooth_point(self, x, y):
        if self.map[y][x] is None:
            return
        border = self.get_border(x, y)
        avg: List[int] = []
        for point in border:
            tmp = self.at(point.x, point.y)
            if tmp is not None:
                avg.append(tmp)
        if len(avg) == 0:
            return
        for i in avg:
            if (i > 0 and self.map[y][x] > 0) or (i < 0 and self.map[y][x] < 0):
                return
        self.map[y][x] = np.mean(avg)

    def smooth(self):
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.smooth_point(x, y)

    def avg(self):
        avg = []
        for x in range(0, self.size):
            for y in range(0, self.size):
                if self.map[y][x] is not None:
                    avg.append(self.map[y][x])
        return np.mean(avg)

    def add_chunk_north(self, chunk):
        for i in range(0, self.size):
            self.map[0][i] = chunk.map[self.size - 1][i]

    def add_chunk_south(self, chunk):
        for i in range(0, self.size):
            self.map[self.size - 1][i] = chunk.map[0][i]

    def add_chunk_east(self, chunk):
        for i in range(0, self.size):
            self.map[i][self.size - 1] = chunk.map[i][0]

    def add_chunk_west(self, chunk):
        for i in range(0, self.size):
            self.map[i][0] = chunk.map[i][self.size - 1]

    def get_size(self):
        return self.size

    def gen(self):
        pass

    size = 0
    map = []
    pos = Point(0, 0)
    isGen = False
