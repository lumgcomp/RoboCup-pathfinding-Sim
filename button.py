import pygame
from colors import *


class TextButton(pygame.sprite.Sprite):
    def __init__(self, text, x, y, font, font_color=BLACK, outline=0, outline_color=BLACK):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.text_surface = self.font.render(self.text, True, font_color)
        self.rect = self.text_surface.get_rect(topleft=(x, y))
        self.outline = outline
        self.outline_color = outline_color

    def tick(self) -> bool:
        return self.rect.collidepoint(*pygame.mouse.get_pos())

    def draw(self, screen):
        screen.blit(self.text_surface, (self.x, self.y))
        if self.outline:
            outline_rect = pygame.Rect(self.rect)
            outline_rect.inflate_ip(self.outline, self.outline)
            pygame.draw.rect(screen, self.outline_color, outline_rect, self.outline)
