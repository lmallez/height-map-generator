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
    def __init__(self, size, pos):
        self.size = 2
        for i in range(0, size):
            self.size = self.size * 2 - 1
        self.init_map(self.size)
        self.set_border(self.size)
        self.pos = pos

    def init_map(self, size):
        self.map = [[None for y in range(0, size)] for x in range(0, size)]

    def set_border(self, size, coef=1):
        self.map[0][0] = round(ran.uniform(-coef * size, coef * size))
        self.map[0][self.size - 1] = round(ran.uniform(-coef * size, coef * size))
        self.map[self.size - 1][0] = round(ran.uniform(-coef * size, coef * size))
        self.map[self.size - 1][self.size - 1] = round(ran.uniform(-coef * size, coef * size))

    size = 0
    map = None
    pos = Point(0, 0)


class Map:
    def __init__(self, chunkSize, initChunk=None):
        self.chunkSize = chunkSize
        if initChunk is not None:
            self.map.append(initChunk)
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

    def gen_point(self, chunk, x, y, ptn_list, pad=1, coef=1):
        avg = []
        for ptn in ptn_list:
            tmp = self.get_point(chunk, ptn.x, ptn.y)
            if tmp is not None:
                avg.append(tmp)
        c = ran.uniform(-coef * pad, coef * pad)
        return round((np.mean(avg) if len(avg) > 0 else 0) + c, 3)

    def __gen_cercle_point(self, chunk, x, y, pad=1, coef=1):
        ptn_list = [Point(x - pad, y - pad),
                    Point(x + pad, y - pad),
                    Point(x - pad, y + pad),
                    Point(x + pad, y + pad),
                    Point(x, y - pad),
                    Point(x, y + pad),
                    Point(x - pad, y),
                    Point(x + pad, y)]
        return self.gen_point(chunk, x, y, ptn_list, pad=pad, coef=coef)

    def __get_diamond_chunk(self, chunk, pad, coef=1):
        size = int(chunk.size / pad) - 1
        for y in range(0, size):
            for x in range(0, size):
                if chunk.map[y * pad][x * pad] is not None and chunk.map[y * pad + pad][x * pad + pad] is None:
                    chunk.map[y * pad + pad][x * pad + pad] = self.__gen_cercle_point(chunk, x * pad + pad, y * pad + pad, pad=pad, coef=coef)
        return

    def __gen_square_point(self, chunk, x, y, pad=1, coef=1):
        ptn_list = [Point(x, y - pad),
                    Point(x, y + pad),
                    Point(x - pad, y),
                    Point(x + pad, y)]
        return self.gen_point(chunk, x, y, ptn_list, pad=pad, coef=coef)

    def __gen_square_chunk(self, chunk, pad, coef=1):
        size = int(chunk.size / pad) + (1 if pad != 1 else 0)
        for y in range(0, size):
            for x in range(0, size):
                if chunk.map[y * pad][x * pad] is None:
                    chunk.map[y * pad][x * pad] = self.__gen_cercle_point(chunk, x * pad, y * pad, pad=pad, coef=coef)
        return

    def __gen_chunk_border(self, chunk):
        north = self.chunk_at(chunk.pos.x, chunk.pos.y - 1)
        north_west = self.chunk_at(chunk.pos.x - 1, chunk.pos.y - 1)
        west = self.chunk_at(chunk.pos.x - 1, chunk.pos.y)
        south_west = self.chunk_at(chunk.pos.x - 1, chunk.pos.y + 1)
        south = self.chunk_at(chunk.pos.x, chunk.pos.y + 1)
        south_east = self.chunk_at(chunk.pos.x + 1, chunk.pos.y + 1)
        east = self.chunk_at(chunk.pos.x + 1, chunk.pos.y)
        north_east = self.chunk_at(chunk.pos.x - 1, chunk.pos.y - 1)
        if west is not None or north is not None or north_west is not None:
            chunk.map[0][0] = self.__gen_cercle_point(chunk, 0, 0)
        if north is not None or east is not None or north_east is not None:
            chunk.map[0][chunk.size - 1] = self.__gen_square_point(chunk, chunk.size - 1, 0)
        if east is not None or south is not None or south_east is not None:
            chunk.map[chunk.size - 1][chunk.size - 1] = self.__gen_square_point(chunk, chunk.size - 1, chunk.size - 1)
        if south is not None or west is not None or south_west is not None:
            chunk.map[chunk.size - 1][0] = self.__gen_square_point(chunk, 0, chunk.size - 1)
        return

    def __gen_chunk_size_map(self, x, y):
        self.sizeMap[0].x = x if x < self.sizeMap[0].x else self.sizeMap[0].x
        self.sizeMap[0].y = y if y < self.sizeMap[0].y else self.sizeMap[0].y
        self.sizeMap[1].x = x + 1 if x + 1 > self.sizeMap[1].x else self.sizeMap[1].x
        self.sizeMap[1].y = y + 1 if y + 1 > self.sizeMap[1].y else self.sizeMap[1].y

    def gen_chunk(self, x, y, coef=1):
        if self.chunk_at(x, y) is not None:
            print("Chunk [%d, %d] already loaded" % (x, y), file=sys.stderr)
            return
        chunk = Chunk(self.chunkSize, Point(x, y))
        self.__gen_chunk_border(chunk)
        pad = int((chunk.size - 1) / 2)
        for i in range(1, self.chunkSize + 1):
            self.__get_diamond_chunk(chunk, pad, coef=coef)
            self.__gen_square_chunk(chunk, pad, coef=coef)
            pad = int(pad / 2)
        chunk.pos = Point(x, y)
        self.map.append(chunk)
        self.__gen_chunk_size_map(x, y)
        return

    def gen_zone(self, a, b, coef=1):
        ptn_to = Point(min(a.x, b.x), min(a.y, b.y))
        ptn_from = Point(max(a.x, b.x), max(a.y, b.y))
        for x in range(ptn_to.x, ptn_from.x):
            for y in range(ptn_to.y, ptn_from.y):
                self.gen_chunk(x, y, coef)

    def chunk_at(self, x, y):
        for chunk in self.map:
            if chunk.pos.x == x and chunk.pos.y == y:
                return chunk
        return None

    sizeMap = [Point(0, 0), Point(1, 1)]
    map = []
    chunkSize = 0


if __name__ == '__main__':
    map_size = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    coef = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    map_larg = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    map = Map(map_size)
    map.gen_zone(Point(0, 0), Point(map_larg, map_larg))

    Printer.printMap(map)
