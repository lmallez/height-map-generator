#!/bin/python3
from entities.chunk_DS_biome import ChunkDSBiome
from entities.map import Map
from entities.point import Point


class MapDSBiome(Map):
    def __init__(self, prof, coef=1):
        Map.__init__(self, prof, coef)
        self.gen_chunk(0, 0)

    def create_chunk(self, x, y):
        return ChunkDSBiome(self.prof, pos=Point(x, y), coef=self.chunk_coef)
