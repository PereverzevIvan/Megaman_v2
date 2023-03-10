# -*- coding: utf-8 -*-
from pygame import mixer, display, time
from pygame import init as pg_init
from settings import *
from src.modules.screens import StartScreen, SettingsScreen

mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pg_init()


class App:
    def __init__(self, w: int, h: int):
        self.width = w
        self.height = h
        self.window = display.set_mode((w, h))
        display.set_caption('Mega Man')
        self.clock = time.Clock()

    def run(self):
        while True:
            action = StartScreen(self.window).run()
            if action == 'quit':
                game_end()
            elif action == 'settings':
                action = SettingsScreen(self.window).run()


if __name__ == '__main__':
    game = App(WIDTH, HEIGHT)
    game.run()
