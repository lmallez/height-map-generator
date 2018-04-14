#!/usr/bin/python3

import HeightMapManager as Mgr
import HeightMapPrinter as Printer
import tkinter as tk
import sys


class DiscoverMap:
    def __init__(self, map, canvas):
        self.map = map
        self.canvas = canvas

    def gen_chunk(self):
        self.map.gen_chunk(self.point.x, self.point.y)

    def gen_top(self):
        self.point.y -= 1
        self.gen_chunk()

    def gen_bot(self):
        self.point.y += 1
        self.gen_chunk()

    def gen_left(self):
        self.point.x -= 1
        self.gen_chunk()

    def gen_right(self):
        self.point.x += 1
        self.gen_chunk()

    def print_map(self):
        self.canvas.delete('all')
        chunk_size = 1000 / max(self.map.sizeMap[1].x - self.map.sizeMap[0].x,
                                self.map.sizeMap[1].y - self.map.sizeMap[0].y)
        for chunk in self.map.map:
            chunk_pos = [chunk.pos.x - self.map.sizeMap[0].x,
                         chunk.pos.y - self.map.sizeMap[0].y]
            chunk_pos = [int(chunk_size) * chunk_pos[0] - chunk_pos[0],
                         int(chunk_size) * chunk_pos[1] - chunk_pos[1]]
            Printer.drawChunk(chunk.map, self.canvas, chunk_size, pos=chunk_pos)
        self.canvas.update()

    def key_event(self, event):
        if event.char == 'z':
            self.gen_top()
        elif event.char == 's':
            self.gen_bot()
        elif event.char == 'q':
            self.gen_left()
        elif event.char == 'd':
            self.gen_right()
        self.print_map()

    canvas = None
    map = None
    point = Mgr.Point(0, 0)


def discover_map(map, winSize=1000):
    win = tk.Tk()
    canvas = tk.Canvas(win, width=winSize, height=winSize, background='black')
    discover_map = DiscoverMap(map, canvas)
    win.bind("<Key>", discover_map.key_event)
    discover_map.print_map()
    discover_map.canvas.pack()
    win.mainloop()


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    map = Mgr.Map(arg, coef=10)
    discover_map(map)