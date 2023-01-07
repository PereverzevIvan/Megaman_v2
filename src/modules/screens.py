from pygame import font, surface, display, time
from pygame.constants import *
from pygame import event as pg_event
from settings import *


class InteractionScreen:
    def __init__(self, screen: surface.Surface):
        self.window = screen
        self.w, self.h = screen.get_size()
        self.screen = surface.Surface((self.w, self.h))
        self.music = ''
        self.bg_image = ''
        self.darkening_screen = surface.Surface((self.w, self.h), SRCALPHA)
        self.font_heading = font.Font(None, int(self.w / 12.8))  # font-size: 50
        self.font_text = font.Font(None, int(self.w / 25.6))  # font-size: 25
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
        self.heading = self.font_heading.render('MEGA MAN', True, WHITE)
        self.heading_rect = self.heading.get_rect(center=(self.w // 2, self.h // 9))

        self.variants = [
            self.font_text.render('GAME START', True, WHITE),
            self.font_text.render('SETTINGS', True, WHITE),
            self.font_text.render('QUIT', True, WHITE),
        ]
        self.variants_rect = [
            self.variants[0].get_rect(center=(self.w // 2, self.h // 1.55)),
            self.variants[1].get_rect(center=(self.w // 2, self.h // 1.4)),
            self.variants[2].get_rect(center=(self.w // 2, self.h // 1.28))
        ]

        self.cursor = 0
        self.cursor_image = surface.Surface((self.w // 42, self.w // 42))
        self.cursor_image.fill(RED)
        self.cursor_pos = [(self.w // 2.55, self.h // 1.55), (self.w // 2.55, self.h // 1.4),
                           (self.w // 2.55, self.h // 1.28)]
        self.cursor_rect = self.cursor_image.get_rect(center=self.cursor_pos[self.cursor])

    def move_cursor(self, move: int):
        self.cursor = (self.cursor + move) % 3
        self.cursor_rect.center = self.cursor_pos[self.cursor]

    def action(self):
        if self.cursor == 0:
            return 'start'
        if self.cursor == 1:
            return 'settings'
        return 'quit'

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.screen.blit(self.heading, self.heading_rect)
        [self.screen.blit(self.variants[i], self.variants_rect[i]) for i in range(3)]
        self.screen.blit(self.cursor_image, self.cursor_rect)

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
                    if event.key == K_UP:
                        self.move_cursor(-1)
                    elif event.key == K_DOWN:
                        self.move_cursor(1)
                    if event.key == K_RETURN:
                        run = False
            self.draw()
            self.window.blit(self.screen, (0, 0))
            self.clock.tick(FPS)
            display.update()
        self.attenuation()
        return self.action()


