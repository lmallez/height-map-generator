#!/bin/python3
from entities.chunk import Chunk
from entities.point import Point


class ChunkBiome(Chunk):
    def __init__(self, heat, height, pos=Point(0, 0)):
        self.heat = heat
        self.height = height
        self.pos = pos

    def init_map(self):
        self.heat.init_map()
        self.height.init_map()

    def gen_height(self):
        self.height.gen()

    def gen_heat(self):
        self.heat.gen()

    def gen(self):
        self.gen_height()
        self.gen_heat()

    def set_border(self, coef, avg=0):
        self.height.set_border(coef, avg=avg)
        self.heat.set_border(coef, avg=avg)

    def add_chunk_north(self, chunk):
        self.height.add_chunk_north(chunk.height)
        self.heat.add_chunk_north(chunk.heat)

    def add_chunk_south(self, chunk):
        self.height.add_chunk_south(chunk.height)
        self.heat.add_chunk_south(chunk.heat)

    def add_chunk_east(self, chunk):
        self.height.add_chunk_east(chunk.height)
        self.heat.add_chunk_east(chunk.heat)

    def add_chunk_west(self, chunk):
        self.height.add_chunk_west(chunk.height)
        self.heat.add_chunk_west(chunk.heat)

    def smooth(self):
        self.height.smooth()
        # self.heat.smooth() TODO : add special Heat smooth

    def get_size(self):
        return self.height.get_size()

    def avg(self):
        return self.height.avg()

    pos = None
    heat = None
    height = None
