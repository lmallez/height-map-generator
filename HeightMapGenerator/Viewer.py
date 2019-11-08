#!/bin/python3

import sys
import sdl2.ext
from HeightMapGenerator.entities.MapDSBiome import MapDSBiome
from HeightMapGenerator.printers.PrinterChunkSDL import PrinterChunkSDL
from HeightMapGenerator.printers.PrinterMapBiome import PrinterMapBiome


def run():
    sdl2.ext.init()
    win_size = 1000
    window = sdl2.ext.Window("PHM - Map Viewer", size=(win_size, win_size))
    surface = window.get_surface()

    world_map = MapDSBiome(4, coef=100)
    world_map.gen_chunk(0, 0)
    world_map.gen_chunk(1, 0)
    world_map.gen_chunk(0, 1)
    world_map.gen_chunk(1, 1)

    printer_chk = PrinterChunkSDL(surface, win_size)
    printer_map = PrinterMapBiome(printer_chk)

    printer_map.draw_map(world_map)
    window.show()
    running = True
    hei = True
    hea = True
    have_event = False
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                have_event = True
                if event.key.keysym.sym == sdl2.SDLK_p:
                    world_map.smooth()
                elif event.key.keysym.sym == sdl2.SDLK_u:
                    hei = not hei
                elif event.key.keysym.sym == sdl2.SDLK_i:
                    hea = not hea
                else:
                    have_event = False
        if have_event:
            sdl2.ext.fill(surface, sdl2.ext.Color(0, 0, 0))
            printer_map.draw_map(world_map, hei=hei, hea=hea)
            have_event = False
        window.refresh()


if __name__ == "__main__":
    sys.exit(run())
