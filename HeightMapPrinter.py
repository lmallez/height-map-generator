#!/usr/bin/python3

import HeightMapManager as Mgr
import tkinter as tk
import sys

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def merge(self, color, coef=0.5):
        red = int(abs(self.r * (1 - coef) + color.r * coef))
        yellow = int(abs(self.g * (1 - coef) + color.g * coef))
        blue = int(abs(self.b * (1 - coef) + color.b * coef))
        return Color(red, yellow, blue)

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
    Teinte(150, 300, Color(30, 50, 0), Color(140, 70, 30)),
    Teinte(300, 1000, Color(140, 70, 30), Color(255, 255, 255))
]


def fixColor(color):
    if color < 0:
        color = 0
    elif color > 255:
        color = 255
    return int(color)


def calcColor(val, x, y, min=0, max=255):
    return fixColor(min + max * ((val - x) / (y - x)))


def drawChunk(chunk, canvas, chunkSize, pos=[0, 0]):
    rectSize = chunkSize / len(chunk)
    for y in range(0, len(chunk)):
        for x in range(0, len(chunk)):
            if chunk[y][x] is None:
                continue
            a = int(chunk[y][x])
            isSet = False
            colorval = Color(0, 0, 0)
            for teinte in EarthTexture:
                if teinte.isInside(a):
                    if isSet:
                        colorval.add(teinte.getColor(a))
                    else:
                        colorval = teinte.getColor(a)
                        isSet = True
            canvas.create_rectangle(x * rectSize + pos[0], y * rectSize + pos[1], (x + 1) * rectSize + pos[0], (y + 1) * rectSize + pos[1], fill=colorval.toStr(), outline="")


def printChunk(Chunk, winSize=1000):
    win = tk.Tk()
    canvas = tk.Canvas(win, width=winSize, height=winSize, background='black')
    drawChunk(Chunk, canvas, 1000)
    canvas.pack()
    win.mainloop()


def printMap(map, winSize=1000):
    win = tk.Tk()
    canvas = tk.Canvas(win, width=winSize, height=winSize, background='black')
    chunkSize = winSize / max(map.sizeMap[1].x - map.sizeMap[0].x, map.sizeMap[1].y - map.sizeMap[0].y)
    for chunk in map.map:
        chunkPos = [int(chunkSize) * chunk.pos.x - chunk.pos.x,
                    int(chunkSize) * chunk.pos.y - chunk.pos.y]
        drawChunk(chunk.map, canvas, chunkSize, pos=chunkPos)
    canvas.pack()
    win.mainloop()


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    map = Mgr.Map(arg)
    printChunk(map.chunk_at(0, 0).map)
