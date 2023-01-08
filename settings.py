# -*- coding: utf-8 -*-
# General
with open('pre_settings.txt', mode='r', encoding='utf-8') as file:
    data = [line.strip().split('=')[1] for line in file.readlines()]
    WIDTH = int(data[0])
    HEIGHT = int(data[1])
    MUSIC_V = int(data[2])
    SOUND_V = int(data[3])
    FULL_SCREEN = bool(data[4])
    FPS = 60


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

MAIN_FONT = None


# Functions
def game_end():
    exit(0)
