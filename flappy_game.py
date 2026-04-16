import random
import pygame
import config as cfg
from animation_module import Animator


class FlappyFoxGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(cfg.FONTS_DIR / "Grand9K Pixel.ttf", 24)
        self.big_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9K Pixel.ttf", 32)

        self.fox_anim = Animator(cfg.ASSETS_DIR / "spritesheet_idle_animation.png", 48, 48, scale=4)

        self.fox_x = 120
        self.fox_y = cfg.HEIGHT // 2
        self.fox_velocity = 0
        self.gravity = 0.35
        self.jump_strength = -7.2

        self.fox_width = 48 * 4
        self.fox_height = 48 * 4

        self.pipe_width = 70
        self.pipe_gap = 165
        self.pipe_speed = 3

        self.pipes = []
        self.pipe_timer = 0
        self.pipe_delay = 1400

        self.score = 0
        self.game_over = False

        self.ground_height = 40

        self.reset()

    def reset(self):
        self.fox_y = cfg.HEIGHT // 2
        self.fox_velocity = 0
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False

    def make_pipe(self):
        gap_y = random.randint(120, cfg.HEIGHT - 120 - self.ground_height)
        top_height = gap_y - (self.pipe_gap // 2)
        bottom_y = gap_y + (self.pipe_gap // 2)

        pipe = {
            "x": cfg.WIDTH,
            "top_rect": pygame.Rect(cfg.WIDTH, 0, self.pipe_width, top_height),
            "bottom_rect": pygame.Rect(
                cfg.WIDTH,
                bottom_y,
                self.pipe_width,
                cfg.HEIGHT - bottom_y - self.ground_height
            ),
            "passed": False
        }

        self.pipes.append(pipe)

    def get_fox_rect(self):
        return pygame.Rect(self.fox_x, int(self.fox_y), self.fox_width, self.fox_height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.game_over:
                    self.reset()
                else:
                    self.fox_velocity = self.jump_strength

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 0:
            if self.game_over:
                self.reset()
            else:
                self.fox_velocity = self.jump_strength

    def update(self, dt):
        self.fox_anim.update(dt)

        if self.game_over:
            return

        self.fox_velocity += self.gravity
        self.fox_y += self.fox_velocity

        self.pipe_timer += dt
        if self.pipe_timer >= self.pipe_delay:
            self.pipe_timer = 0
            self.make_pipe()

        for pipe in self.pipes:
            pipe["x"] -= self.pipe_speed
            pipe["top_rect"].x = pipe["x"]
            pipe["bottom_rect"].x = pipe["x"]

            if not pipe["passed"] and pipe["x"] + self.pipe_width < self.fox_x:
                pipe["passed"] = True
                self.score += 1

        self.pipes = [pipe for pipe in self.pipes if pipe["x"] + self.pipe_width > 0]

        fox_rect = self.get_fox_rect()

        if fox_rect.top <= 0:
            self.game_over = True

        if fox_rect.bottom >= cfg.HEIGHT - self.ground_height:
            self.game_over = True

        for pipe in self.pipes:
            if fox_rect.colliderect(pipe["top_rect"]) or fox_rect.colliderect(pipe["bottom_rect"]):
                self.game_over = True

    def draw_background(self):
        self.screen.fill((170, 220, 255))

        ground_rect = pygame.Rect(0, cfg.HEIGHT - self.ground_height, cfg.WIDTH, self.ground_height)
        pygame.draw.rect(self.screen, (100, 180, 100), ground_rect)

    def draw_pipes(self):
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (60, 180, 75), pipe["top_rect"])
            pygame.draw.rect(self.screen, (60, 180, 75), pipe["bottom_rect"])

            top_cap = pygame.Rect(pipe["top_rect"].x - 4, pipe["top_rect"].bottom - 20, self.pipe_width + 8, 20)
            bottom_cap = pygame.Rect(pipe["bottom_rect"].x - 4, pipe["bottom_rect"].y, self.pipe_width + 8, 20)

            pygame.draw.rect(self.screen, (40, 140, 55), top_cap)
            pygame.draw.rect(self.screen, (40, 140, 55), bottom_cap)

    def draw_fox(self):
        self.fox_anim.draw(self.screen, self.fox_x, int(self.fox_y))

    def draw_ui(self):
        score_text = self.font.render(f"score: {self.score}", True, cfg.BLACK)
        self.screen.blit(score_text, (20, 20))

        if self.game_over:
            over_text = self.big_font.render("game over", True, cfg.BLACK)
            restart_text = self.font.render("press space or click to restart", True, cfg.BLACK)

            over_x = (cfg.WIDTH - over_text.get_width()) // 2
            restart_x = (cfg.WIDTH - restart_text.get_width()) // 2

            self.screen.blit(over_text, (over_x, 170))
            self.screen.blit(restart_text, (restart_x, 230))
        else:
            help_text = self.font.render("space or click = flap", True, cfg.BLACK)
            help_x = (cfg.WIDTH - help_text.get_width()) // 2
            self.screen.blit(help_text, (help_x, 20))

    def draw(self):
        self.draw_background()
        self.draw_pipes()
        self.draw_fox()
        self.draw_ui()

    def run(self):
        running = True

        while running:
            dt = self.clock.tick(cfg.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                self.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "exit"

            self.update(dt)
            self.draw()
            pygame.display.flip()

        return "exit"


def run_flappy_game():
    pygame.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Flappy Fox")
    game = FlappyFoxGame(screen)
    return game.run()


if __name__ == "__main__":
    run_flappy_game()