#!/bin/python3

import sdl2.ext
from draw.PrinterChunk import PrinterChunk


class PrinterChunkSDL(PrinterChunk):
    def __init__(self, surface, win_size, hei_pal=None, hea_pal=None):
        PrinterChunk.__init__(self, win_size, hei_pal, hea_pal)
        self.surface = surface

    def print(self, color, area):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(int(color.r), int(color.g), int(color.b)), area=area)

    surface = None