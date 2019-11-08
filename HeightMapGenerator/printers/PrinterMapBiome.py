#!/bin/python3

from HeightMapGenerator.printers.PrinterMap import PrinterMap


class PrinterMapBiome(PrinterMap):
    def __init__(self, printer_chunk):
        PrinterMap.__init__(self, printer_chunk)

    def get_hei_buffer(self, chunk):
        return chunk.height.map

    def get_hea_buffer(self, chunk):
        return chunk.heat.map
