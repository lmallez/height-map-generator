#!/usr/bin/python3

import tkinter as tk
import HeightMapGenerator
import sys

def drawMap(map, canvas, winSize):
    rectSize = round(winSize / len(map))
    for y in range(0, len(map)):
        for x in range(0, len(map)):
            a = int(map[x][y])
            if a > 10:
                blue = 0
            else:
                blue = 255 - 255 * ((a + 30) / 50)
            if a < 0:
                red = 0
            else:
                red = 255 * (a / 50)
            colorval = "#%02x%02x%02x" % (int(red), 0, int(blue))
            canvas.create_rectangle(x * rectSize, y * rectSize, (x + 1) * rectSize, (y + 1) * rectSize, fill=colorval, outline="")

def printMap(map):
    win = tk.Tk()
    mapSize = 800
    canvas = tk.Canvas(win, width=mapSize, height=mapSize, background='black')
    drawMap(map, canvas, mapSize)
    canvas.pack()
    win.mainloop()


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    printMap(HeightMapGenerator.genMap(arg))
