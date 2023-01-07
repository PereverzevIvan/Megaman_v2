# -*- coding: utf-8 -*-
from pygame import font, surface, display, time, mouse
from pygame.constants import *
from pygame import event as pg_event
from src.modules.gui_elems import Label, Button, Slider
from settings import *


class InteractionScreen:
    def __init__(self, screen: surface.Surface):
        self.window = screen
        self.w, self.h = screen.get_size()
        self.screen = surface.Surface((self.w, self.h))
        self.music = ''
        self.bg_image = ''
        self.darkening_screen = surface.Surface((self.w, self.h), SRCALPHA)
        self.heading_font_size = int(self.w / 8)
        self.text_font_size = int(self.w / 20)
        self.clock = time.Clock()
        self.cursor = 0

        self.begin = True

    def rising(self):
        for i in range(26):
            self.darkening_screen.fill((0, 0, 0, 250 - 10 * i))
            self.window.blit(self.screen, (0, 0))
            self.window.blit(self.darkening_screen, (0, 0))
            self.clock.tick(FPS // 2.1)
            display.update()

    def attenuation(self):
        for i in range(1, 26):
            self.darkening_screen.fill((0, 0, 0, 10 * i))
            self.window.blit(self.screen, (0, 0))
            self.window.blit(self.darkening_screen, (0, 0))
            self.clock.tick(FPS // 2.1)
            display.update()


class StartScreen(InteractionScreen):
    def __init__(self, screen: surface.Surface):
        super(StartScreen, self).__init__(screen)
        self.bg_image = surface.Surface((self.w, self.h))
        self.bg_image.fill(BLACK)
        self.heading = Label(int(self.w // 2), int(self.h // 8.5), self.heading_font_size, 'MEGA MAN', self.screen)

        self.variants = [
            Button(int(self.w // 2), int(self.h // 1.6), self.text_font_size, 'GAME START', self.screen, 0),
            Button(int(self.w // 2), int(self.h // 1.4), self.text_font_size, 'SETTINGS', self.screen, 1),
            Button(int(self.w // 2), int(self.h // 1.24), self.text_font_size, 'QUIT', self.screen, 2)
        ]

    def action(self):
        if self.cursor == 0:
            return 'start'
        if self.cursor == 1:
            return 'settings'
        return 'quit'

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.heading.draw()
        [self.variants[i].draw() for i in range(3)]

        if self.begin:
            self.rising()
            self.begin = False

    def run(self):
        run = True
        while run:
            for event in pg_event.get():
                if event.type == QUIT:
                    game_end()
                if event.type == KEYDOWN:
                    pass
                    if event.key == K_RETURN:
                        run = False
                if event.type == MOUSEMOTION:
                    hovers = [btn.check_hover(mouse.get_pos()) for btn in self.variants]
                    if any(hovers):
                        if self.cursor != hovers.index(True):
                            self.cursor = hovers.index(True)
                if event.type == MOUSEBUTTONDOWN:
                    presses = [btn.check_press(mouse.get_pos()) for btn in self.variants]
                    if any(presses):
                        run = False

            self.draw()
            self.window.blit(self.screen, (0, 0))
            self.clock.tick(FPS)
            display.update()
        self.attenuation()
        return self.action()


class SettingsScreen(InteractionScreen):
    def __init__(self, screen: surface.Surface):
        super(SettingsScreen, self).__init__(screen)
        self.heading = Label(int(self.w // 2), int(self.h // 8.5), self.heading_font_size, 'SETTINGS', self.screen)
        self.bg_image = surface.Surface((self.w, self.h))
        self.bg_image.fill(BLACK)

        self.btn_save = Button(int(self.w // 2.5), int(self.h // 1.1),
                               self.text_font_size, '    SAVE    ', self.screen, 0)
        self.btn_def = Button(int(self.w // 1.64), int(self.h // 1.1), self.text_font_size, 'DEFAULT', self.screen, 0)

        self.slider_volume = Slider(WIDTH // 2, HEIGHT // 2, 200, 30, self.screen)

        self.btns = [self.btn_save, self.btn_def]

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.heading.draw()

        self.btn_save.draw()
        self.btn_def.draw()
        self.slider_volume.draw()

        if self.begin:
            self.rising()
            self.begin = False

    def run(self):
        run = True
        while run:
            mouse_pos = mouse.get_pos()
            for event in pg_event.get():
                if event.type == QUIT:
                    game_end()
                if event.type == KEYDOWN:
                    pass
                    if event.key == K_RETURN:
                        run = False
                if event.type == MOUSEMOTION:
                    hovers = [btn.check_hover(mouse_pos) for btn in self.btns]
                    if any(hovers):
                        if self.cursor != hovers.index(True):
                            self.cursor = hovers.index(True)
                    self.slider_volume.check_hover(mouse_pos)
                if event.type == MOUSEBUTTONDOWN:
                    if self.btn_save.check_press(mouse.get_pos()):
                        run = False
                    self.slider_volume.check_press(mouse_pos)
                if event.type == MOUSEBUTTONUP:
                    if self.slider_volume.was_press:
                        self.slider_volume.was_press = False

            self.slider_volume.update_pos(mouse_pos)
            self.draw()
            self.window.blit(self.screen, (0, 0))
            self.clock.tick(FPS)
            display.update()
        self.attenuation()
        return None
