#!/bin/python3
from entities.pallet import Pallet
from entities.point import Point
from entities.tint import Tint, Color


class PrinterChunk:
    def __init__(self, win_size, hei_pal=None, hea_pal=None):
        self.win_size = win_size
        if hea_pal is not None:
            self.hei_pal = hei_pal
        if hea_pal is not None:
            self.hea_pal = hea_pal

    def print(self, color, area):
        raise NotImplementedError("Should have implemented this")

    @staticmethod
    def get_rect(rect_size, x, y, pos_x, pos_y):
        return [
            int(x * rect_size + pos_x),
            int(y * rect_size + pos_y),
            rect_size + 1,
            rect_size + 1,
        ]

    def print_chunk(self, buffer, pallet, pos=Point(0, 0), size=0):
        if size == 0:
            size = self.win_size
        rect_size = size / len(buffer)
        for y in range(0, len(buffer) - 1):
            for x in range(0, len(buffer) - 1):
                if buffer[y] is None or buffer[y][x] is None:
                    continue
                color_val = pallet.get_color(buffer[y][x])
                self.print(color_val, self.get_rect(rect_size, x, y, pos.x, pos.y))

    def print_mix_chunk(self, hei_buffer, hea_buffer, pos=Point(0, 0), size=0):
        if size == 0:
            size = self.win_size
        rect_size = size / len(hei_buffer)
        for y in range(0, len(hei_buffer) - 1):
            for x in range(0, len(hei_buffer) - 1):
                if hei_buffer[y] is None or hei_buffer[y][x] is None:
                    continue
                hei_col = self.hei_pal.get_color(hei_buffer[y][x])
                hea_col = self.hea_pal.get_color(hea_buffer[y][x])
                if hei_buffer[y][x] >= 0:
                    hei_col.merge(hea_col, 0.3)
                self.print(hei_col, self.get_rect(rect_size, x, y, pos.x, pos.y))

    def draw_chunk(
        self, hei_buffer, hea_buffer, hea=True, hei=True, pos=Point(0, 0), size=0
    ):
        if size == 0:
            size = self.win_size

        if hea and hei and hea_buffer is not None and hei_buffer is not None:
            self.print_mix_chunk(hei_buffer, hea_buffer, pos=pos, size=size)
        elif hea and hea_buffer is not None:
            self.print_chunk(hea_buffer, self.hea_pal, pos=pos, size=size)
        elif hei and hei_buffer is not None:
            self.print_chunk(hei_buffer, self.hei_pal, pos=pos, size=size)

    surface = None
    win_size = 0
    hea_pal = Pallet(
        [
            Tint(-100, -80, Color(255, 255, 255), Color(255, 255, 255)),
            Tint(-80, -10, Color(128, 128, 0), Color(128, 128, 0)),
            Tint(-10, 70, Color(127, 255, 0), Color(127, 255, 0)),
            Tint(70, 101, Color(255, 255, 102), Color(255, 255, 102)),
        ]
    )
    hei_pal = Pallet(
        [
            Tint(-100, 0, Color(0, 0, 50), Color(1, 120, 180)),
            Tint(0, 101, Color(0, 0, 0), Color(255, 255, 255)),
        ]
    )
