#!/usr/bin/python3

import sys
import HeightMapPrinter as Printer
import numpy as np
import random as ran


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    x = 0
    y = 0


class Chunk:
    def __init__(self, size, pos, coef=1):
        self.size = 2
        for i in range(0, size):
            self.size = self.size * 2 - 1
        self.init_map(self.size)
        self.set_border(self.size, coef)
        self.pos = pos

    def init_map(self, size):
        self.map = [[None for y in range(0, size)] for x in range(0, size)]

    def set_border(self, size, coef):
        self.map[0][0] = round(ran.uniform(-coef * size, coef * size))
        self.map[0][self.size - 1] = round(ran.uniform(-coef * size, coef * size))
        self.map[self.size - 1][0] = round(ran.uniform(-coef * size, coef * size))
        self.map[self.size - 1][self.size - 1] = round(ran.uniform(-coef * size, coef * size))

    size = 0
    map = None
    pos = Point(0, 0)


class Map:
    def __init__(self, chunkSize, init_chunk=None, coef=0):
        self.chunkSize = chunkSize
        self.coef = coef
        if init_chunk is not None:
            self.map.append(init_chunk)
        else:
            self.gen_chunk(0, 0)

    def get_point(self, chunk, x, y):
        if 0 <= x < chunk.size and 0 <= y < chunk.size:
            return chunk.map[y][x]
        chunk_pos = Point(chunk.pos.x, chunk.pos.y)

        if x < 0:
            chunk_pos.x += int(x / chunk.size) - 1
            x = chunk.size - (abs(x) % chunk.size)
        elif x >= chunk.size:
            chunk_pos.x += int(x / chunk.size)
            x = abs(x) % chunk.size
        if y < 0:
            chunk_pos.y += int(y / chunk.size) - 1
            y = chunk.size - (abs(y) % chunk.size)
        elif y >= chunk.size:
            chunk_pos.y += int(y / chunk.size)
            y = abs(y) % chunk.size
        tmp_chunk = self.chunk_at(chunk_pos.x, chunk_pos.y)
        if tmp_chunk is None:
            return None
        return tmp_chunk.map[y][x]

    def gen_point(self, chunk, x, y, ptn_list, pad=1):
        avg = []
        for ptn in ptn_list:
            aled = None
            while ptn.x - x != 0 or ptn.y - y != 0:
                tmp = self.get_point(chunk, ptn.x, ptn.y)
                if ptn.x - x != 0:
                    ptn.x = ptn.x - 1 if ptn.x - x > 0 else ptn.x + 1
                if ptn.y - y != 0:
                    ptn.y = ptn.y - 1 if ptn.y - y > 0 else ptn.y + 1
                if tmp is not None:
                    aled = tmp
            if aled is not None:
                avg.append(aled)
        c = ran.uniform(-self.coef * pad, self.coef * pad)
        return round((np.mean(avg) if len(avg) > 0 else 0) + c, 3)

    def __gen_cercle_point(self, chunk, x, y, pad=1):
        ptn_list = [Point(x - pad, y - pad),
                    Point(x + pad, y - pad),
                    Point(x - pad, y + pad),
                    Point(x + pad, y + pad),
                    Point(x, y - pad),
                    Point(x, y + pad),
                    Point(x - pad, y),
                    Point(x + pad, y)]
        return self.gen_point(chunk, x, y, ptn_list, pad=pad)

    def __get_diamond_chunk(self, chunk, pad):
        size = int(chunk.size / pad) - 1
        for y in range(0, size):
            for x in range(0, size):
                if chunk.map[y * pad][x * pad] is not None and chunk.map[y * pad + pad][x * pad + pad] is None:
                    chunk.map[y * pad + pad][x * pad + pad] = self.__gen_cercle_point(chunk, x * pad + pad, y * pad + pad, pad=pad)
        return

    def __gen_square_point(self, chunk, x, y, pad=1):
        ptn_list = [Point(x, y - pad),
                    Point(x, y + pad),
                    Point(x - pad, y),
                    Point(x + pad, y)]
        return self.gen_point(chunk, x, y, ptn_list, pad=pad)

    def __gen_square_chunk(self, chunk, pad):
        size = int(chunk.size / pad) + (1 if pad != 1 else 0)
        for y in range(0, size):
            for x in range(0, size):
                if chunk.map[y * pad][x * pad] is None:
                    chunk.map[y * pad][x * pad] = self.__gen_cercle_point(chunk, x * pad, y * pad, pad=pad)
        return

    def __gen_chunk_border(self, chunk):
        north = self.chunk_at(chunk.pos.x, chunk.pos.y - 1)
        west = self.chunk_at(chunk.pos.x - 1, chunk.pos.y)
        south = self.chunk_at(chunk.pos.x, chunk.pos.y + 1)
        east = self.chunk_at(chunk.pos.x + 1, chunk.pos.y)

        if north is not None:
            for i in range(0, chunk.size):
                chunk.map[0][i] = north.map[chunk.size - 1][i]
        if west is not None:
            for i in range(0, chunk.size):
                chunk.map[i][0] = west.map[i][chunk.size - 1]
        if south is not None:
            for i in range(0, chunk.size):
                chunk.map[chunk.size - 1][i] = south.map[0][i]
        if east is not None:
            for i in range(0, chunk.size):
                chunk.map[i][chunk.size - 1] = east.map[i][0]
        return

    def __gen_chunk_size_map(self, x, y):
        self.sizeMap[0].x = x if x < self.sizeMap[0].x else self.sizeMap[0].x
        self.sizeMap[0].y = y if y < self.sizeMap[0].y else self.sizeMap[0].y
        self.sizeMap[1].x = x + 1 if x + 1 > self.sizeMap[1].x else self.sizeMap[1].x
        self.sizeMap[1].y = y + 1 if y + 1 > self.sizeMap[1].y else self.sizeMap[1].y

    def gen_chunk(self, x, y):
        if self.chunk_at(x, y) is not None:
            print("Chunk [%d, %d] already loaded" % (x, y), file=sys.stderr)
            return
        chunk = Chunk(self.chunkSize, Point(x, y))
        self.__gen_chunk_border(chunk)
        pad = int((chunk.size - 1) / 2)
        for i in range(1, self.chunkSize + 1):
            self.__get_diamond_chunk(chunk, pad)
            self.__gen_square_chunk(chunk, pad)
            pad = int(pad / 2)
        chunk.pos = Point(x, y)
        self.map.append(chunk)
        self.__gen_chunk_size_map(x, y)
        return

    def gen_zone(self, a, b):
        ptn_to = Point(min(a.x, b.x), min(a.y, b.y))
        ptn_from = Point(max(a.x, b.x), max(a.y, b.y))
        for x in range(ptn_to.x, ptn_from.x):
            for y in range(ptn_to.y, ptn_from.y):
                self.gen_chunk(x, y)

    def chunk_at(self, x, y):
        for chunk in self.map:
            if chunk.pos.x == x and chunk.pos.y == y:
                return chunk
        return None

    sizeMap = [Point(0, 0), Point(1, 1)]
    coef = 1
    map = []
    chunkSize = 0


if __name__ == '__main__':
    map_size = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    coef = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    map_larg = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    map = Map(map_size, coef=10)
    map.gen_zone(Point(0, 0), Point(map_larg, map_larg))

    Printer.printMap(map)
