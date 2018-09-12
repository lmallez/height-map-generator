import sys
import sdl2
import sdl2.ext
import Printer
import random as ran
from entity.ChunkDS import ChunkDS

def run():
    ran.seed(2917)
    sdl2.ext.init()
    chunk = ChunkDS(6, coef=10)
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
        sdl2.ext.fill(surface, sdl2.ext.Color(0, 0, 0))
        Printer.drawChunk(surface, chunk.map, 1000)
        window.refresh()


if __name__ == "__main__":
    sys.exit(run())