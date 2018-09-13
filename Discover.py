#!/usr/bin/python3

import sys

import sdl2.ext

from draw.PrinterChunkSDL import PrinterChunkSDL
from draw.PrinterMapBiom import PrinterMapBiom
from entity.MapDSBiom import MapDSBiom
from entity.Point import Point


class DiscoverMap:
    def __init__(self, map):
        self.map = map

    def gen_chunk(self, force=False):
        self.map.gen_chunk(self.point.x, self.point.y, force=force)

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

    def smooth(self):
        self.map.smooth()

    def regen(self):
        self.gen_chunk(force=True)

    def delete(self):
        self.map.delete(self.point.x, self.point.y)

    def height_view(self):
        self.hei = not self.hei

    def heat_view(self):
        self.hea = not self.hea

    def print(self, printer):
        printer.draw_map(map, hei=self.hei, hea=self.hea)

    hei = True
    hea = True
    map = None
    point = Point(0, 0)


map_key = {
    sdl2.SDLK_UP: DiscoverMap.gen_top,
    sdl2.SDLK_LEFT: DiscoverMap.gen_left,
    sdl2.SDLK_RIGHT: DiscoverMap.gen_right,
    sdl2.SDLK_DOWN: DiscoverMap.gen_bot,
    sdl2.SDLK_p: DiscoverMap.smooth,
    sdl2.SDLK_m: DiscoverMap.regen,
    sdl2.SDLK_o: DiscoverMap.delete,
    sdl2.SDLK_u: DiscoverMap.height_view,
    sdl2.SDLK_i: DiscoverMap.heat_view
}

def run(map):
    sdl2.ext.init()
    discover_map = DiscoverMap(map)

    winsize = 1000
    window = sdl2.ext.Window("Height Map Discover", size=(1000, 1000))
    window.show()
    surface = window.get_surface()

    printer_chk = PrinterChunkSDL(surface, winsize)
    printer_map = PrinterMapBiom(printer_chk)

    running = True
    edit = True
    while running:
        if edit:
            sdl2.ext.fill(surface, sdl2.ext.Color(0, 0, 0))
            discover_map.print(printer_map)
            window.refresh()
            edit = False
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym in map_key:
                    edit = True
                    map_key[event.key.keysym.sym](discover_map)
                else:
                    edit = False
            elif event.type == sdl2.SDL_QUIT:
                running = False


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    map = MapDSBiom(arg, coef=30)
    run(map)