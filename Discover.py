#!/usr/bin/python3

import sys
import BiomPrinter
from entity.Point import Point
from entity.ChunkDS import ChunkDS
from entity.MapDS import MapDS
import sdl2.ext


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

    def regen(self):
        self.gen_chunk(force=True)

    def delete(self):
        self.map.delete(self.point.x, self.point.y)

    def print_map(self, surface):
        chunk_size = 1000 / max(self.map.sizeMap[1].x - self.map.sizeMap[0].x,
                                self.map.sizeMap[1].y - self.map.sizeMap[0].y)
        for pos, chunk in self.map.map.items():
            chunk_pos = [chunk.pos.x - self.map.sizeMap[0].x,
                         chunk.pos.y - self.map.sizeMap[0].y]
            chunk_pos = [int(chunk_size) * chunk_pos[0] - chunk.pos.x * chunk_size / self.map.chunk_size,
                         int(chunk_size) * chunk_pos[1] - chunk.pos.y * chunk_size / self.map.chunk_size]
            BiomPrinter.drawChunk(surface, chunk.height.map, chunk.heat.map, chunk_size, pos=chunk_pos)
            if chunk.pos.x == self.point.x and chunk.pos.y == self.point.y:
                sdl2.ext.fill(surface, sdl2.ext.Color(255, 0, 0), area=[chunk_pos[0] + chunk_size / 2, chunk_pos[1] + chunk_size / 2, 10, 10])

    map = None
    point = Point(0, 0)


def run(map):
    sdl2.ext.init()
    discover_map = DiscoverMap(map)

    window = sdl2.ext.Window("Height Map Discover", size=(1000, 1000))
    window.show()
    surface = window.get_surface()
    running = True
    edit = True
    while running:
        if edit:
            edit = False
            sdl2.ext.fill(surface, sdl2.ext.Color(0, 0, 0))
            discover_map.print_map(surface)
            window.refresh()
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                edit = True
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    discover_map.gen_top()
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    discover_map.gen_left()
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    discover_map.gen_right()
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    discover_map.gen_bot()
                elif event.key.keysym.sym == sdl2.SDLK_p:
                    discover_map.map.smooth()
                elif event.key.keysym.sym == sdl2.SDLK_m:
                    discover_map.regen()
                elif event.key.keysym.sym == sdl2.SDLK_o:
                    discover_map.delete()
                else:
                    edit = False
            elif event.type == sdl2.SDL_QUIT:
                running = False


if __name__ == '__main__':
    arg = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    map = MapDS(arg, coef=10)
    run(map)