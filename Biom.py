#!/bin/python3
import sys
import sdl2
import sdl2.ext
import BiomPrinter
from entity.ChunkDSBiom import ChunkDSBiom
import random as ran


def run():
    ran.seed(3929)
    sdl2.ext.init()
    chunk = ChunkDSBiom(8, min=-49, max=49, coef=10)
    chunk.gen()
    window = sdl2.ext.Window("The Pong Game", size=(1000, 1000))
    window.show()
    surface = window.get_surface()
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_p:
                    chunk.smooth()
                elif event.key.keysym.sym == sdl2.SDLK_o:
                    chunk.regen()
        BiomPrinter.printChunk(surface, chunk.height, chunk.heat)
        window.refresh()
    return 0


if __name__ == "__main__":
    sys.exit(run())
