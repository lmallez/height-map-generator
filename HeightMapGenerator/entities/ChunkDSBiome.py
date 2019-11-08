#!/bin/python3

from HeightMapGenerator.entities.ChunkBiome import ChunkBiome
from HeightMapGenerator.entities.ChunkDS import ChunkDS
from HeightMapGenerator.entities.Point import Point


class ChunkDSBiome(ChunkBiome):
    def __init__(self, size, pos=Point(0, 0), coef=1, min=-100, max=100):
        ChunkBiome.__init__(self, ChunkDS(size, pos, coef, min, max), ChunkDS(size, pos, coef, min, max))
