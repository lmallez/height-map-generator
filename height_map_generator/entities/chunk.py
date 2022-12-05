#!/bin/python3


class Chunk:
    def init_map(self):
        raise NotImplementedError("Should have implemented this")

    def gen(self):
        raise NotImplementedError("Should have implemented this")

    def regen(self):
        self.init_map()
        self.gen()

    def set_border(self, coef, avg=0):
        raise NotImplementedError("Should have implemented this")

    def add_chunk_north(self, chunk):
        raise NotImplementedError("Should have implemented this")

    def add_chunk_south(self, chunk):
        raise NotImplementedError("Should have implemented this")

    def add_chunk_east(self, chunk):
        raise NotImplementedError("Should have implemented this")

    def add_chunk_west(self, chunk):
        raise NotImplementedError("Should have implemented this")

    def smooth(self):
        raise NotImplementedError("Should have implemented this")

    def get_size(self):
        raise NotImplementedError("Should have implemented this")
