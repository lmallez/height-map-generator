#!/usr/bin/python3

import tkinter as tk
from entity.Teinte import Teinte, Color
from entity.Point import Point
from sdl2 import ext, rect, sdlgfx
import sdl2

ext.init()

EarthTexture = [
    # Teinte(-255, 0, Color(0, 0, 0), Color(0, 0, 255)),
    # Teinte(-50, 0, Color(0, 0, 0), Color(0, 100, 0)),
    # Teinte(0, 150, Color(0, 200, 0), Color(30, 50, 0)),
    # Teinte(150, 300, Color(30, 50, 0), Color(140, 70, 30)),
    # Teinte(300, 1000, Color(140, 70, 30), Color(255, 255, 255))
    Teinte(-100, 0, Color(0, 0, 255), Color(0, 0, 100)),
    Teinte(0, 101, Color(100, 100, 100), Color(255, 255, 255))
]


def fixColor(color):
    if color < 0:
        color = 0
    elif color > 255:
        color = 255
    return int(color)


def calcColor(val, x, y, min=0, max=255):
    return fixColor(min + max * ((val - x) / (y - x)))


def getEarthColor(val, pallette):
    isSet = False
    colorval = Color(0, 0, 0)
    for teinte in pallette:
        if teinte.isInside(val):
            if isSet:
                colorval.add(teinte.getColor(val))
            else:
                colorval = teinte.getColor(val)
                isSet = True
    return colorval


def drawChunk(window, buffer, size, pos=[0, 0], pallette=EarthTexture):
    rectSize = size / len(buffer)
    for y in range(0, len(buffer) - 1):
        for x in range(0, len(buffer) - 1):
            if buffer[y] is None or buffer[y][x]is None:
                continue
            colorval = getEarthColor(buffer[y][x], pallette)
            my_rect = [
                int(x * rectSize + pos[0]),
                int(y * rectSize + pos[1]),
                rectSize,
                rectSize
            ]
            sdl2.ext.fill(window, sdl2.ext.Color(colorval.r, colorval.g, colorval.b), area=my_rect)


def printChunk(window, chunk, size=1000, pallette=EarthTexture):
    drawChunk(window, chunk.map, size, pallette=pallette)
