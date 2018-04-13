#!/usr/bin/python3

import csv
import sys
import HeightMapPrinter as Printer


def read_chunk(name):
    with open(name) as file:
        return [[int(j) for j in l[:-1].split(",")] for l in file]


if __name__ == '__main__':
    map = readFile(sys.argv[1])
    Printer.printChunk(map)