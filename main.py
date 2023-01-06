from pygame import rect, font, surface, mixer, display, time
from pygame.constants import *
from pygame import event as pg_event, init as pg_init


class App:
    def __init__(self, w: int, h: int):
        self.width = w
        self.height = h
        self.window = display.set_mode((w, h))
        self.fps = 60
        self.clock = time.Clock()

    def run(self):
        run = True
        while run:
            for event in pg_event.get():
                if event.type == QUIT:
                    run = False


if __name__ == '__main__':
    game = App(1280, 720)
    game.run()
