#!/bin/python3

from entity.Map import Map
from entity.ChunkDSBiom import ChunkDSBiom
from entity.Point import Point


class MapDSBiom(Map):
    def __init__(self, prof, coef=1):
        Map.__init__(self, prof, coef)
        self.gen_chunk(0, 0)

    def create_chunk(self, x, y):
        return ChunkDSBiom(self.prof, pos=Point(x, y), coef=self.chunk_coef)