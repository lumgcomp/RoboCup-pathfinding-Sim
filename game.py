import pygame.sprite
from constants import *
from objects import Pitch, Ball, Player, Ennemy
from button import TextButton
from selector import Selector

ball_image = pygame.image.load("assets/ball.png")
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))

pitch_image = pygame.image.load("assets/pitch.png")
pitch_image = pygame.transform.scale(pitch_image, (WIDTH, HEIGHT))

player_image = pygame.image.load("assets/player.png")
player_image = pygame.transform.scale(player_image, PLAYER_SIZE)

enemy_image = pygame.image.load("assets/ennemy.png")
enemy_image = pygame.transform.scale(enemy_image, PLAYER_SIZE)


class Game:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win

        self.pitch = Pitch(pitch_image, WIDTH // 2, HEIGHT // 2)
        self.ball = Ball(ball_image, 0, 0)
        self.ball.init_random_position(self.pitch)

        self.player = Player(player_image, 0, 0)
        self.player.init_random_position(self.pitch)

        self.enemies = [Ennemy(enemy_image, 0, 0), Ennemy(enemy_image, 0, 0)]
        for ennemy in self.enemies:
            ennemy.init_random_position(self.pitch)
            self.pitch.add_ennemy(ennemy.i, ennemy.j)

        self.sprites = [self.ball, self.player, *self.enemies]
        self.last_positions = [self.player.rect.center, self.ball.rect.center]
        ennemies_last_positions = [ennemy.rect.center for ennemy in self.enemies]
        self.last_positions.extend(ennemies_last_positions)  # format is [player, ball, ennemy1, ennemy2, ... ]

        # buttons
        font = pygame.font.SysFont("Arial", 30)
        self.buttons = []
        self.btn_go_to_ball = TextButton("Go to ball", WIDTH // 2 - 200, 20, font, BLUE, outline=2, outline_color=BLUE)
        self.btn_restart = TextButton("Restart", WIDTH // 2 - 40, 20, font, RED, outline=2, outline_color=RED)
        self.btn_reset = TextButton("Reset", WIDTH // 2 + 100, 20, font, BLACK, outline=2, outline_color=BLACK)
        self.buttons.extend([self.btn_go_to_ball, self.btn_restart, self.btn_reset])

        # label
        self.time_elapsed = 0
        self.timer_on = False

        self.selector = Selector(["a_star", "dijkstra", "dfs", "bfs", "aca"])

    def run(self):
        clock = pygame.time.Clock()
        while self.game_is_on:
            dt = clock.tick(FPS)
            if self.timer_on:
                self.time_elapsed += dt
                if not self.player.path:
                    self.timer_on = False
            self.events()
            self.update(dt)
            self.draw(self.win)

    def events(self):
        events = pygame.event.get()
        self.selector.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.game_is_on = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_go_to_ball.tick():
                    self.player.find_path_to(self.ball, self.pitch, self.selector.options[self.selector.selected])
                    self.timer_on = True
                    self.time_elapsed = 0
                elif self.btn_restart.tick():
                    self.last_positions = [self.player.rect.center, self.ball.rect.center]
                    ennemies_last_positions = [ennemy.rect.center for ennemy in self.enemies]
                    self.last_positions.extend(ennemies_last_positions)
                    self.ball.init_random_position(self.pitch)
                    self.player.init_random_position(self.pitch)
                    for ennemy in self.enemies:
                        self.pitch.remove_ennemy(ennemy.i, ennemy.j)
                        ennemy.init_random_position(self.pitch)
                        self.pitch.add_ennemy(ennemy.i, ennemy.j)
                    self.player.path = []

                elif self.btn_reset.tick():
                    # set the last positions
                    self.player.rect.center = self.last_positions[0]
                    self.ball.rect.center = self.last_positions[1]
                    for i, ennemy in enumerate(self.enemies):
                        ennemy.rect.center = self.last_positions[i + 2]

                    self.player.path = []

    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)

    def draw(self, win):
        win.fill(GREEN)
        self.pitch.draw(win, draw_grid=True)
        for sprite in self.sprites:
            sprite.draw(win)

        # buttons
        for button in self.buttons:
            button.draw(win)

        # label
        font = pygame.font.SysFont("Arial", 30)
        timer_label = font.render(f"Timer : {self.time_elapsed / 1000:.2f}s", True, BLACK)
        surface = pygame.Surface(timer_label.get_size())

        surface.fill(WHITE)
        x, y = WIDTH // 2, 100
        surface.blit(timer_label, (0, 0))

        win.blit(surface, surface.get_rect(center=(x, y)))

        self.selector.draw(win, 100, 20)
        pygame.display.flip()
