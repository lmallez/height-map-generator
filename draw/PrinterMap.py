#!/bin/python3

from entity.Point import Point


class PrinterMap:
    def __init__(self, printer_chunk):
        self.printer_chunk = printer_chunk

    def get_hei_buffer(self, chunk):
        raise NotImplementedError("Should have implemented this")

    def get_hea_buffer(self, chunk):
        raise NotImplementedError("Should have implemented this")

    def draw_chunk(self, chunk, chunk_pos, chunk_size, hei, hea):
        self.printer_chunk.draw_chunk(
            self.get_hei_buffer(chunk),
            self.get_hea_buffer(chunk),
            hei=hei, hea=hea, pos=chunk_pos, size=chunk_size
        )

    def draw_map(self, map, hei=True, hea=True):
        chunk_size = 1000 / max(map.size_map.y.x - map.size_map.x.x,
                                map.size_map.y.y - map.size_map.x.y)
        for pos, chunk in map.map.items():
            chunk_pos = [chunk.pos.x - map.size_map.x.x,
                         chunk.pos.y - map.size_map.x.y]
            chunk_pos = Point(int(chunk_size) * chunk_pos[0] - chunk.pos.x * chunk_size / map.chunk_size,
                              int(chunk_size) * chunk_pos[1] - chunk.pos.y * chunk_size / map.chunk_size)
            self.draw_chunk(chunk, chunk_pos, chunk_size, hei, hea)

    printer_chunk = None