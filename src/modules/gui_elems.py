# -*- coding: utf-8 -*-
from pygame import font, rect, surface, draw
from pygame.constants import SRCALPHA
from settings import *


class Label:
    def __init__(self, c_x: int, c_y: int, ft_sz: int, text: str, screen: surface.Surface):
        self.screen = screen
        self.font = font.Font(MAIN_FONT, ft_sz)
        self.text = text
        self.text_surface = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(c_x, c_y))
        self.w, self.h = self.text_rect.size

    def draw(self):
        self.screen.blit(self.text_surface, self.text_rect)

    def change_text(self, text: str):
        self.text_surface = self.font.render(text, True, WHITE)

    def change_color(self, color: (int, int, int)):
        self.text_surface = self.font.render(self.text, True, color)


class Button(Label):
    def __init__(self, c_x: int, c_y: int, ft_sz: int, text: str, screen: surface.Surface, s_id: int):
        super(Button, self).__init__(c_x, c_y, ft_sz, text, screen)
        self.id = s_id
        self.hover = False
        self.was_press = False
        self.border_color = GRAY
        self.border_color_hover = WHITE
        self.border_rect = rect.Rect(0, 0, self.w * 1.1, self.h * 1.3)
        self.border_rect.center = self.text_rect.center
        self.fill_surface = surface.Surface(self.border_rect.size, SRCALPHA)
        self.fill_color = (255, 255, 255, 50)
        self.fill_surface.fill(self.fill_color)

    def draw(self):
        if self.hover and not self.was_press:
            self.screen.blit(self.fill_surface, self.border_rect)
            draw.rect(self.screen, self.border_color_hover, self.border_rect, width=2)
        else:
            draw.rect(self.screen, self.border_color, self.border_rect, width=2)
        self.screen.blit(self.text_surface, self.text_rect)

    def change_border_color(self, color: (int, int, int)):
        self.border_color = color

    def change_fill_color(self, color: (int, int, int, int)):
        self.fill_color = color
        self.fill_surface.fill(self.fill_color)

    def check_hover(self, mouse_pos: (int, int)):
        self.hover = self.text_rect.collidepoint(mouse_pos)
        return self.hover

    def check_press(self, mouse_pos: (int, int)):
        self.was_press = self.text_rect.collidepoint(mouse_pos)
        return self.was_press


class Slider:
    def __init__(self, c_x: int, c_y: int, w: int, h: int, screen: surface.Surface):
        self.rect = rect.Rect(0, 0, w, h)
        self.rect.center = (c_x, c_y)
        self.screen = screen

        self.cursor = surface.Surface((h * 0.5, h * 1.2))
        self.cursor_rect = self.cursor.get_rect(center=(self.rect.left, self.rect.centery))
        self.cursor_pos = 0
        self.cursor_states = [int(w // 100 * i) for i in range(101)]

        self.fill_rect = self.rect.copy()
        self.fill_rect.w = self.cursor_states[self.cursor_pos]

        self.label = Label(self.rect.right + 20, self.rect.centery, self.rect.w // 8, str(self.cursor_pos), self.screen)

        self.hover = False
        self.was_press = False

        self.border_color = GRAY
        self.fill_color = WHITE

    def draw(self):
        draw.rect(self.screen, self.fill_color, self.fill_rect)
        draw.rect(self.screen, self.border_color, self.rect, width=2)
        if self.hover or self.was_press:
            draw.rect(self.screen, self.fill_color, self.cursor_rect)
        else:
            draw.rect(self.screen, self.border_color, self.cursor_rect)
        self.label.draw()

    def update_cursor_rect(self, cursor_pos):
        self.cursor_rect.centerx = self.rect.left + self.cursor_states[cursor_pos]

    def update_pos(self, mouse_pos: (int, int)):
        x, y = mouse_pos
        if self.was_press:
            if self.rect.left - 50 <= x <= self.rect.right + 50:
                x = min(self.rect.right, x)
                x = max(self.rect.left, x)
                difference = x - self.rect.left
                if difference in self.cursor_states:
                    self.cursor_pos = self.cursor_states.index(difference)
                    self.update_cursor_rect(self.cursor_pos)
                    self.fill_rect.w = self.cursor_states[self.cursor_pos]
                    self.label.change_text(str(self.cursor_pos))

    def check_hover(self, mouse_pos: (int, int)):
        self.hover = self.cursor_rect.collidepoint(mouse_pos)
        return self.hover

    def check_press(self, mouse_pos: (int, int)):
        self.was_press = self.cursor_rect.collidepoint(mouse_pos)
        return self.was_press
