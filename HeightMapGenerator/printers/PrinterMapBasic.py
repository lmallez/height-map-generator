#!/bin/python3

from HeightMapGenerator.printers.PrinterMap import PrinterMap


class PrinterMapBasic(PrinterMap):
    def __init__(self, printer_chunk):
        PrinterMap.__init__(self, printer_chunk)

    def get_hei_buffer(self, chunk):
        return chunk.map

    def get_hea_buffer(self, chunk):
        return None
