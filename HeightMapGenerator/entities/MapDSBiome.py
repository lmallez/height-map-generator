#!/bin/python3

from HeightMapGenerator.entities.Map import Map
from HeightMapGenerator.entities.ChunkDSBiome import ChunkDSBiome
from HeightMapGenerator.entities.Point import Point


class MapDSBiome(Map):
    def __init__(self, prof, coef=1):
        Map.__init__(self, prof, coef)
        self.gen_chunk(0, 0)

    def create_chunk(self, x, y):
        return ChunkDSBiome(self.prof, pos=Point(x, y), coef=self.chunk_coef)
