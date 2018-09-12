#!/bin/python3

from entity.ChunkBiom import ChunkBiom
from entity.ChunkDS import ChunkDS
from entity.Point import Point


class ChunkDSBiom(ChunkBiom):
    def __init__(self, size, pos=Point(0, 0), coef=1, min=-100, max=100):
        ChunkBiom.__init__(self,
            ChunkDS(size, pos, coef, min, max),
            ChunkDS(size, pos, coef, min, max)
        )

