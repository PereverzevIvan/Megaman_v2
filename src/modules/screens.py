from pygame import font, surface, display, time, mouse
from pygame.constants import *
from pygame import event as pg_event
from src.modules.gui_elems import Label, Button
from settings import *


class InteractionScreen:
    def __init__(self, screen: surface.Surface):
        self.window = screen
        self.w, self.h = screen.get_size()
        self.screen = surface.Surface((self.w, self.h))
        self.music = ''
        self.bg_image = ''
        self.darkening_screen = surface.Surface((self.w, self.h), SRCALPHA)
        self.heading_font_size = int(self.w / 12.8)  # font-size: 50
        self.text_font_size = int(self.w / 25.6)  # font-size: 25
        self.clock = time.Clock()

        self.begin = True

    def rising(self):
        for i in range(26):
            self.darkening_screen.fill((0, 0, 0, 250 - 10 * i))
            self.window.blit(self.screen, (0, 0))
            self.window.blit(self.darkening_screen, (0, 0))
            self.clock.tick(FPS // 2)
            display.update()

    def attenuation(self):
        for i in range(1, 26):
            self.darkening_screen.fill((0, 0, 0, 10 * i))
            self.window.blit(self.screen, (0, 0))
            self.window.blit(self.darkening_screen, (0, 0))
            self.clock.tick(FPS // 2)
            display.update()


class StartScreen(InteractionScreen):
    def __init__(self, screen: surface.Surface):
        super(StartScreen, self).__init__(screen)
        self.bg_image = surface.Surface((self.w, self.h))
        self.bg_image.fill(BLACK)
        self.heading = Label(self.w // 2, self.h // 9, self.heading_font_size, 'MEGA MAN', self.screen)

        self.variants = [
            Button(int(self.w // 2), int(self.h // 1.55), self.text_font_size, 'GAME START', self.screen, 0),
            Button(int(self.w // 2), int(self.h // 1.4), self.text_font_size, 'SETTINGS', self.screen, 1),
            Button(int(self.w // 2), int(self.h // 1.28), self.text_font_size, 'QUIT', self.screen, 2)
        ]

        self.cursor = 0

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


