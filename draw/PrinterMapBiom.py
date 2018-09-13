#!/bin/python3

from draw.PrinterMap import PrinterMap


class PrinterMapBiom(PrinterMap):
    def __init__(self, printer_chunk):
        PrinterMap.__init__(self, printer_chunk)

    def get_hei_buffer(self, chunk):
        return chunk.height.map

    def get_hea_buffer(self, chunk):
        return chunk.heat.map
