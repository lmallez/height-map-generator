#!/usr/bin/python3

import tkinter as tk
import HeightMapGenerator as HeightMapGenerator
import sys


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def merge(self, color, coef=0.5):
        red = int(abs(self.r * (1 - coef) + color.r * coef))
        green = int(abs(self.g * (1 - coef) + color.g * coef))
        blue = int(abs(self.b * (1 - coef) + color.b * coef))
        return Color(red, green, blue)

    def add(self, color):
        self.r += color.r
        self.g += color.g
        self.b += color.b
        return

    def toStr(self):
        return "#%02x%02x%02x" % (self.r, self.g, self.b)

    r = 0
    g = 0
    b = 0


class Teinte:
    def __init__(self, x, y, min, max):
        self.min = min
        self.max = max
        self.x = x
        self.y = y

    def isInside(self, x):
        return self.x <= x and x < self.y

    def getColor(self, x):
        diff = (x - self.x) / (self.y - self.x)
        return self.min.merge(self.max, coef=diff)

    min = Color
    max = Color
    x = 0
    y = 0


EarthTexture = [
    Teinte(-255, 0, Color(0, 0, 0), Color(0, 0, 255)),
    Teinte(-50, 0, Color(0, 0, 0), Color(0, 100, 0)),
    Teinte(0, 150, Color(0, 200, 0), Color(30, 50, 0)),
    Teinte(150, 200, Color(30, 50, 0), Color(140, 70, 30)),
    Teinte(200, 500, Color(140, 70, 30), Color(255, 255, 255))
]


def fixColor(color):
    if color < 0:
        color = 0
    elif color > 255:
        color = 255
    return int(color)


def calcColor(val, x, y, min=0, max=255):
    return fixColor(min + max * ((val - x) / (y - x)))


def drawMap(map, canvas, winSize):
    rectSize = round(winSize / len(map))
    for y in range(0, len(map)):
        for x in range(0, len(map)):
            a = int(map[y][x])
            isSet = False
            colorval = Color(0, 0, 0)
            for teinte in EarthTexture:
                if teinte.isInside(a):
                    if isSet:
                        colorval.add(teinte.getColor(a))
                    else:
                        colorval = teinte.getColor(a)
                        isSet = True
            canvas.create_rectangle(x * rectSize, y * rectSize, (x + 1) * rectSize, (y + 1) * rectSize, fill=colorval.toStr(), outline="")


def printMap(map):
    win = tk.Tk()
    mapSize = 1000
    canvas = tk.Canvas(win, width=mapSize, height=mapSize, background='black')
    drawMap(map, canvas, mapSize)
    canvas.pack()
    win.mainloop()


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    printMap(HeightMapGenerator.genMap(arg))
