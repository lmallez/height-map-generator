#!/bin/python3

import random as ran
import numpy as np
from HeightMapGenerator.entities.ChunkBasic import ChunkBasic, Point


class ChunkDS(ChunkBasic):
    def __init__(self, size, pos=Point(0, 0), coef=1, min=-100, max=100):
        ChunkBasic.__init__(self, size, pos, coef)
        self.coef = coef
        self.min = min
        self.max = max

    def gen_point(self, ptn_list, pad=1):
        avg = []
        for ptn in ptn_list:
            tmp = self.at(ptn.x, ptn.y)
            if tmp is not None:
                avg.append(tmp)
        c = ran.uniform(-self.coef * 0.5 * pad, self.coef * 0.5 * pad)
        d = round((np.mean(avg) if len(avg) > 0 else 0) + c, 3)
        if d > self.max:
            d = self.max
        if d < self.min:
            d = self.min
        return d

    def gen_circle_point(self, x, y, pad=1):
        ptn_list = [Point(x - pad, y - pad),
                    Point(x + pad, y - pad),
                    Point(x - pad, y + pad),
                    Point(x + pad, y + pad),
                    Point(x, y - pad),
                    Point(x, y + pad),
                    Point(x - pad, y),
                    Point(x + pad, y)]
        return self.gen_point(ptn_list, pad=pad)

    def get_diamond_chunk(self, pad):
        size = int(self.size / pad) - 1
        for y in range(0, size):
            for x in range(0, size):
                if self.map[y * pad][x * pad] is not None and self.map[y * pad + pad][x * pad + pad] is None:
                    self.map[y * pad + pad][x * pad + pad] = \
                        self.gen_circle_point(x * pad + pad, y * pad + pad, pad=pad)
        return

    def gen_square_point(self, x, y, pad=1):
        ptn_list = [Point(x, y - pad),
                    Point(x, y + pad),
                    Point(x - pad, y),
                    Point(x + pad, y)]
        return self.gen_point(ptn_list, pad=pad)

    def gen_square_chunk(self, pad):
        size = int(self.size / pad) + (1 if pad != 1 else 0)
        for y in range(0, size):
            for x in range(0, size):
                if self.map[y * pad][x * pad] is None:
                    self.map[y * pad][x * pad] = self.gen_circle_point(x * pad, y * pad, pad=pad)
        return

    def gen(self):
        pad = int(self.size / 2)
        while pad > 0:
            self.get_diamond_chunk(pad)
            self.gen_square_chunk(pad)
            pad = int(pad / 2)
        return

    coef = 0
    min = 0
    max = 0
