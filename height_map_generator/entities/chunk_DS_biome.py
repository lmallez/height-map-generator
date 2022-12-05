#!/bin/python3
from entities.chunk_biome import ChunkBiome
from entities.chunk_DS import ChunkDS
from entities.point import Point


class ChunkDSBiome(ChunkBiome):
    def __init__(self, size, pos=Point(0, 0), coef=1, min=-100, max=100):
        ChunkBiome.__init__(
            self,
            ChunkDS(size, pos, coef, min, max),
            ChunkDS(size, pos, coef, min, max),
        )
