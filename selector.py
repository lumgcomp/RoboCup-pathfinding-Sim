import pygame

pygame.font.init()

FONT = pygame.font.SysFont("None", 30)
COLOR_DEFAULT = (20,60, 240)
COLOR_SELECTED = (255, 0, 0)


class Selector:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.x = 0
        self.y = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)

    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        for i, option in enumerate(self.options):
            if i == self.selected:
                message = FONT.render(option, True, COLOR_SELECTED)
            else:
                message = FONT.render(option, True, COLOR_DEFAULT)
            message_rect = message.get_rect(center=(x, y + i * message.get_height()))
            screen.blit(message, message_rect)
