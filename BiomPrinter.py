#!/bin/python3

import sdl2.ext
from entity.Teinte import Color, Teinte
from Printer import getEarthColor

HeatTexture = [
    Teinte(-100, -80, Color(255, 255, 255), Color(255, 255, 255)),
    Teinte(-80, -10, Color(128, 128, 0), Color(128, 128, 0)),
    Teinte(-10, 70, Color(127, 255, 0), Color(127, 255, 0)),
    Teinte(70, 100, Color(255, 255, 102), Color(255, 255, 102))
]

EarthTexture = [
    Teinte(-100, 0, Color(0, 0, 50), Color(1, 120, 180)),
    Teinte(0, 101, Color(0, 0, 0), Color(255, 255, 255))
]


def drawChunk(window, earthbuffer, heatbuffer, size, pos=[0, 0], earthPallette=EarthTexture, heatPallette=HeatTexture):
    rectSize = size / len(earthbuffer)
    for y in range(0, len(earthbuffer) - 1):
        for x in range(0, len(earthbuffer) - 1):
            if earthbuffer[y] is None or earthbuffer[y][x]is None:
                continue

            earthcolor = getEarthColor(earthbuffer[y][x], earthPallette)
            heatcolor = getEarthColor(heatbuffer[y][x], heatPallette)

            if earthbuffer[y][x] >= 0:
                earthcolor.merge(heatcolor, 0.3)

            my_rect = [
                int(x * rectSize + pos[0]),
                int(y * rectSize + pos[1]),
                rectSize + 1,
                rectSize + 1
            ]
            sdl2.ext.fill(window, sdl2.ext.Color(earthcolor.r, earthcolor.g, earthcolor.b), area=my_rect)


def printChunk(window, chunk, heat, size=1000):
    drawChunk(window, chunk.map, heat.map, size)
