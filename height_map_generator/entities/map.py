#!/bin/python3

import sys

from entities.point import Point


class Map:
    def __init__(self, prof, coef=1):
        self.prof = prof
        self.chunk_size = 2
        self.chunk_coef = coef
        for i in range(0, prof):
            self.chunk_size = self.chunk_size * 2 - 1

    def create_chunk(self, x, y):
        raise NotImplementedError("Should have implemented this")

    def smooth(self):
        for pos, chunk in self.map.items():
            chunk.smooth()

    def get_point(self, chunk_x, chunk_y, x, y):
        if 0 <= x < self.chunk_size and 0 <= y < self.chunk_size:
            return self.chunk_at(chunk_x, chunk_y)[y][x]
        chunk_pos = Point(chunk_x, chunk_y)
        if x < 0:
            chunk_pos.x += int(x / self.chunk_size) - 1
            x = self.chunk_size - (abs(x) % self.chunk_size)
        elif x >= self.chunk_size:
            chunk_pos.x += int(x / self.chunk_size)
            x = abs(x) % self.chunk_size
        if y < 0:
            chunk_pos.y += int(y / self.chunk_size) - 1
            y = self.chunk_size - (abs(y) % self.chunk_size)
        elif y >= self.chunk_size:
            chunk_pos.y += int(y / self.chunk_size)
            y = abs(y) % self.chunk_size
        tmp_chunk = self.chunk_at(chunk_pos.x, chunk_pos.y)
        if tmp_chunk is None:
            return None
        return tmp_chunk.map[y][x]

    def __gen_chunk_border(self, chunk):
        north = self.chunk_at(chunk.pos.x, chunk.pos.y - 1)
        west = self.chunk_at(chunk.pos.x - 1, chunk.pos.y)
        south = self.chunk_at(chunk.pos.x, chunk.pos.y + 1)
        east = self.chunk_at(chunk.pos.x + 1, chunk.pos.y)

        if north is not None:
            chunk.add_chunk_north(north)
        if west is not None:
            chunk.add_chunk_west(west)
        if south is not None:
            chunk.add_chunk_south(south)
        if east is not None:
            chunk.add_chunk_east(east)
        chunk.set_border(self.chunk_coef, chunk.avg())

    def gen_chunk(self, x, y, force=False):
        if force is False and self.chunk_at(x, y) is not None:
            print("Chunk [%d, %d] already loaded" % (x, y), file=sys.stderr)
            return
        chunk = self.create_chunk(x, y)
        chunk.pos = Point(x, y)
        self.__gen_chunk_border(chunk)
        chunk.gen()
        self.map[x + y * 1000] = chunk
        self.update_map_size(x, y)
        return

    def delete(self, x, y):
        del self.map[x + y * 1000]

    def update_map_size(self, x, y):
        self.size_map.x.x = x if x < self.size_map.x.x else self.size_map.x.x
        self.size_map.x.y = y if y < self.size_map.x.y else self.size_map.x.y
        self.size_map.y.x = x + 1 if x + 1 > self.size_map.y.x else self.size_map.y.x
        self.size_map.y.y = y + 1 if y + 1 > self.size_map.y.y else self.size_map.y.y

    def chunk_at(self, x, y):
        return self.map.get(x + y * 1000)

    map = dict()
    chunk_size = 0
    chunk_coef = 0
    prof = 0
    size_map = Point(Point(0, 0), Point(1, 1))
