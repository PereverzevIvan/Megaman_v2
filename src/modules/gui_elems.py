# -*- coding: utf-8 -*-
from pygame import draw
from pygame.constants import SRCALPHA
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.font import Font
from pygame.transform import scale, rotate
from settings import *


class Label:
    def __init__(self, c_x: int, c_y: int, ft_sz: int, text: str, screen: Surface):
        self.screen = screen
        self.font = Font(MAIN_FONT, ft_sz)
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
    def __init__(self, c_x: int, c_y: int, ft_sz: int, text: str, screen: Surface):
        super(Button, self).__init__(c_x, c_y, ft_sz, text, screen)
        self.hover = False
        self.was_press = False
        self.border_color = GRAY
        self.border_color_hover = WHITE
        self.border_rect = Rect(0, 0, self.w * 1.1, self.h * 1.3)
        self.border_rect.center = self.text_rect.center
        self.fill_surface = Surface(self.border_rect.size, SRCALPHA)
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
        self.hover = self.border_rect.collidepoint(mouse_pos)
        return self.hover

    def check_press(self, mouse_pos: (int, int)):
        self.was_press = self.border_rect.collidepoint(mouse_pos)
        return self.was_press

    def change_rect(self, self_side: str, other_side: int):
        if self_side == 'right':
            self.border_rect.right = other_side
        if self_side == 'left':
            self.border_rect.left = other_side
        if self_side == 'top':
            self.border_rect.top = other_side
        if self_side == 'bottom':
            self.border_rect.bottom = other_side
        self.text_rect.center = self.border_rect.center


class Slider:
    def __init__(self, c_x: int, c_y: int, w: int, h: int, screen: Surface):
        self.rect = Rect(0, 0, w, h)
        self.rect.center = (c_x, c_y)
        self.screen = screen

        self.cursor_image = Surface((h * 0.5, h * 1.2))
        self.cursor_rect = self.cursor_image.get_rect(center=(self.rect.left, self.rect.centery))
        self.cursor = 0
        self.cursor_states = [int(w // 100 * i) for i in range(101)]

        self.fill_rect = self.rect.copy()
        self.fill_rect.w = self.cursor_states[self.cursor]

        self.label = Label(self.rect.right + WIDTH // 32, self.rect.centery, self.rect.w // 8, str(self.cursor),
                           self.screen)

        self.hover = False
        self.was_press = False

        self.border_color = GRAY
        self.fill_color = WHITE

    def set_cursor(self, cursor):
        self.cursor = cursor
        self.cursor_rect.centerx = self.rect.left + self.cursor_states[self.cursor]
        self.fill_rect.w = self.cursor_states[self.cursor]
        self.label.change_text(str(self.cursor))

    def draw(self):
        draw.rect(self.screen, self.fill_color, self.fill_rect)
        draw.rect(self.screen, self.border_color, self.rect, width=2)
        if self.hover or self.was_press:
            draw.rect(self.screen, self.fill_color, self.cursor_rect)
        else:
            draw.rect(self.screen, self.border_color, self.cursor_rect)
        self.label.draw()

    def define_cursor_pos(self, difference):
        for state in self.cursor_states:
            if difference <= state:
                return state

    def update_pos(self, mouse_pos: (int, int)):
        x, y = mouse_pos
        if self.was_press:
            x = min(self.rect.right, x)
            x = max(self.rect.left, x)
            difference = self.define_cursor_pos(x - self.rect.left)
            self.cursor = self.cursor_states.index(difference)
            self.cursor_rect.centerx = x
            self.fill_rect.w = difference
            self.label.change_text(str(self.cursor))

    def check_hover(self, mouse_pos: (int, int)):
        self.hover = self.cursor_rect.collidepoint(mouse_pos)
        return self.hover

    def check_press(self, mouse_pos: (int, int)):
        self.was_press = self.cursor_rect.collidepoint(mouse_pos)
        return self.was_press

    def return_value(self):
        return self.cursor


class ButtonWithImage(Button):
    def __init__(self, c_x: int, c_y: int, w: int, h: int, image: Surface, screen: Surface):
        super(ButtonWithImage, self).__init__(c_x, c_y, 0, '0', screen)
        self.screen = screen
        self.border_rect = Rect(0, 0, w, h)
        self.border_rect.center = (c_x, c_y)
        self.image = scale(image, self.border_rect.size)
        self.fill_surface = Surface(self.border_rect.size, SRCALPHA)
        self.fill_surface.fill(self.fill_color)

    def draw(self):
        self.screen.blit(self.image, self.border_rect)
        if self.hover and not self.was_press:
            self.screen.blit(self.fill_surface, self.border_rect)
            draw.rect(self.screen, self.border_color_hover, self.border_rect, width=2)
        else:
            draw.rect(self.screen, self.border_color, self.border_rect, width=2)

    def check_press(self, mouse_pos: (int, int)):
        return self.border_rect.collidepoint(mouse_pos)


class SpinBox(Label):
    def __init__(self, c_x: int, c_y: int, ft_sz: int, variants, screen: Surface):
        super(SpinBox, self).__init__(c_x, c_y, ft_sz, '', screen)
        self.variants = variants
        self.screen = screen
        self.text_color = WHITE
        self.border_color = GRAY
        self.rect = self.init_rect(c_x, c_y)
        btn_image = self.generate_btn_image()

        self.btn_left = ButtonWithImage(self.rect.left - self.rect.h // 2, c_y,
                                        self.rect.h, self.rect.h, rotate(btn_image, 180), screen)
        self.btn_left.change_rect('right', self.rect.left)
        self.btn_right = ButtonWithImage(self.rect.right + self.rect.h // 2, c_y,
                                         self.rect.h, self.rect.h, btn_image, screen)
        self.btn_right.change_rect('left', self.rect.right)

        self.text = [self.font.render(line, True, self.text_color) for line in variants]
        self.text_rects = [line.get_rect(center=(c_x, c_y)) for line in self.text]

        self.cursor = 0

    def generate_btn_image(self):
        h = self.rect.h
        image = Surface((h, h))
        poits = ((h // 4, h // 4), (h // 4, h * 0.75), (h * 0.75, h // 2))
        draw.polygon(image, self.text_color, poits)
        return image

    def update_cursor(self, action):
        self.cursor = (self.cursor + action) % len(self.variants)

    def init_rect(self, c_x, c_y):
        max_line = max(self.variants, key=len)
        text = self.font.render(max_line, True, self.text_color)
        rect = text.get_rect()
        rect.size = rect.size[0] * 1.1, rect.size[1] * 1.3
        rect.center = (c_x, c_y)
        return rect

    def render_text(self):
        for line in self.variants:
            self.text += [self.font.render(line, True, self.text_color)]

    def draw(self):
        draw.rect(self.screen, self.border_color, self.rect, width=2)
        self.btn_right.draw()
        self.btn_left.draw()
        self.screen.blit(self.text[self.cursor], self.text_rects[self.cursor])

    def check_hover(self, mouse_pos: (int, int)):
        self.btn_left.check_hover(mouse_pos)
        self.btn_right.check_hover(mouse_pos)

    def update(self, mouse_pos: (int, int)):
        if self.btn_left.check_press(mouse_pos):
            self.update_cursor(-1)
        if self.btn_right.check_press(mouse_pos):
            self.update_cursor(1)

    def return_value(self):
        return self.variants[self.cursor]
