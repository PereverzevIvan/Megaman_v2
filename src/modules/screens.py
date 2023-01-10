# -*- coding: utf-8 -*-
from pygame import display, time, mouse
from pygame.constants import *
from pygame.surface import Surface
from pygame import event as pg_event
from src.modules.gui_elems import Label, Button, Slider, SpinBox
from settings import *


class InteractionScreen:
    def __init__(self, screen: Surface):
        self.window = screen
        self.w, self.h = screen.get_size()
        self.screen = Surface((self.w, self.h))
        self.music = ''
        self.bg_image = ''
        self.darkening_screen = Surface((self.w, self.h), SRCALPHA)
        self.heading_font_size = int(self.w / 8)
        self.text_font_size = int(self.w / 18)
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
    def __init__(self, screen: Surface):
        super(StartScreen, self).__init__(screen)
        self.bg_image = Surface((self.w, self.h))
        self.bg_image.fill(BLACK)
        self.heading = Label(int(self.w // 2), int(self.h // 8.5), self.heading_font_size, 'MEGA MAN', self.screen)

        self.variants = [
            Button(int(self.w // 2), int(self.h // 1.75), self.text_font_size, 'GAME START', self.screen),
            Button(int(self.w // 2), int(self.h // 1.45), self.text_font_size, 'SETTINGS', self.screen),
            Button(int(self.w // 2), int(self.h // 1.24), self.text_font_size, 'QUIT', self.screen)
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
    def __init__(self, screen: Surface):
        super(SettingsScreen, self).__init__(screen)
        self.heading = Label(int(self.w // 2), int(self.h // 8.5), self.heading_font_size, 'SETTINGS', self.screen)
        self.bg_image = Surface((self.w, self.h))
        self.bg_image.fill(BLACK)
        self.label_font_size = int(WIDTH // 20)

        self.btn_cancel = None
        self.btn_save = None
        self.btns = None
        self.sound_slider = None
        self.music_slider = None
        self.sliders = None
        self.fullscreen_spinbox = None
        self.resolution_spinbox = None
        self.spinboxes = None
        self.generate_inputs()

        self.label_sound = None
        self.label_music = None
        self.label_full_screen = None
        self.label_res = None
        self.labels = []
        self.generate_labels()

        self.move_slider = False

    def generate_labels(self):
        self.label_res = Label(WIDTH // 6.5, HEIGHT // 3.8, self.label_font_size, 'RESOLUTION', self.screen)
        self.label_full_screen = Label(WIDTH // 6.5, HEIGHT // 2.43,
                                       self.label_font_size, 'FULL SCREEN', self.screen)
        self.label_music = Label(WIDTH // 6.5, HEIGHT // 1.35,
                                 self.label_font_size, 'MUSIC', self.screen)
        self.label_sound = Label(WIDTH // 6.5, HEIGHT // 1.75,
                                 self.label_font_size, 'SOUND', self.screen)
        self.labels = [self.label_res, self.label_full_screen, self.label_music, self.label_sound]

    def generate_inputs(self):
        self.btn_save = Button(int(self.w // 2.5), int(self.h // 1.1), self.text_font_size, '    SAVE    ', self.screen)
        self.btn_cancel = Button(int(self.w // 1.64), int(self.h // 1.1), self.text_font_size, 'CANCEL', self.screen)
        self.btns = [self.btn_save, self.btn_cancel]

        self.music_slider = Slider(WIDTH // 1.35, HEIGHT // 1.35, round(WIDTH / 3.2), HEIGHT // 12, self.screen)
        self.sound_slider = Slider(WIDTH // 1.35, HEIGHT // 1.75, round(WIDTH / 3.2), HEIGHT // 12, self.screen)
        self.music_slider.set_cursor(MUSIC_V)
        self.sound_slider.set_cursor(SOUND_V)
        self.sliders = [self.sound_slider, self.music_slider]

        resolution_variants = ['640x360', '1280x720', '1600x900', '1920x1080']
        full_screen_variants = [' YES ', ' NO ']
        cur_res = f'{WIDTH}x{HEIGHT}'
        cur_fullscreen = ' YES ' if FULL_SCREEN else ' NO '
        self.fullscreen_spinbox = SpinBox(WIDTH // 1.35, HEIGHT // 2.43, int(WIDTH // 18.2),
                                          full_screen_variants, self.screen)
        self.resolution_spinbox = SpinBox(WIDTH // 1.35, HEIGHT // 3.8, int(WIDTH // 18.2),
                                          resolution_variants, self.screen)
        self.resolution_spinbox.cursor = resolution_variants.index(cur_res)
        self.fullscreen_spinbox.cursor = full_screen_variants.index(cur_fullscreen)
        self.spinboxes = [self.fullscreen_spinbox, self.resolution_spinbox]

    def save_settings(self):
        pass

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.heading.draw()
        self.btn_save.draw()
        self.btn_cancel.draw()
        self.music_slider.draw()
        [slider.draw() for slider in self.sliders]
        [spinbox.draw() for spinbox in self.spinboxes]
        [label.draw() for label in self.labels]

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
                    [btn.check_hover(mouse_pos) for btn in self.btns]
                    [slider.check_hover(mouse_pos) for slider in self.sliders]
                    [spinbox.check_hover(mouse_pos) for spinbox in self.spinboxes]
                if event.type == MOUSEBUTTONDOWN:
                    if self.btn_save.check_press(mouse.get_pos()):
                        run = False
                        self.save_settings()
                    slider_presses = [slider.check_press(mouse_pos) for slider in self.sliders]
                    if any(slider_presses) and not self.move_slider:
                        self.move_slider = True
                    [spinbox.update(mouse_pos) for spinbox in self.spinboxes]

                if event.type == MOUSEBUTTONUP:
                    for slider in self.sliders:
                        slider.was_press = False
                    self.move_slider = False

            if self.move_slider:
                [slider.update_pos(mouse_pos) for slider in self.sliders]
            self.draw()
            self.window.blit(self.screen, (0, 0))
            self.clock.tick(FPS)
            display.update()
        self.attenuation()
        return None
