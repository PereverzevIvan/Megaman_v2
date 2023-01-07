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
