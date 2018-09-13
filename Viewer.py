#!/bin/python3

import sys
import sdl2.ext
from entity.MapDSBiom import MapDSBiom
from draw.PrinterChunkSDL import PrinterChunkSDL
from draw.PrinterMapBiom import PrinterMapBiom

def run():
    sdl2.ext.init()
    winsize = 1000
    window = sdl2.ext.Window("PHM - Map Viewer", size=(winsize, winsize))
    surface = window.get_surface()

    map = MapDSBiom(6, coef=10)
    map.gen_chunk(0, 0)
    map.gen_chunk(1, 0)
    map.gen_chunk(0, 1)
    map.gen_chunk(1, 1)

    printer_chk = PrinterChunkSDL(surface, winsize)
    printer_map = PrinterMapBiom(printer_chk)

    printer_map.draw_map(map)
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
                    map.smooth()
                elif event.key.keysym.sym == sdl2.SDLK_u:
                    hei = not hei
                elif event.key.keysym.sym == sdl2.SDLK_i:
                    hea = not hea
                else:
                    have_event = False
        if have_event:
            sdl2.ext.fill(surface, sdl2.ext.Color(0, 0, 0))
            printer_map.draw_map(map, hei=hei, hea=hea)
            have_event = False
        window.refresh()


if __name__ == "__main__":
    sys.exit(run())