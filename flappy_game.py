import random
import pygame
import config as cfg



class FlappyFoxGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(cfg.FONTS_DIR / "Grand9K Pixel.ttf", 24)
        self.big_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9K Pixel.ttf", 32)
        self.small_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9K Pixel.ttf", 16)

        # Scale 2 gives a 96x96 fox — reasonable for a flappy game on 500x500
        raw_head = pygame.image.load(cfg.ASSETS_DIR / "flappy_head.png").convert()
        raw_head.set_colorkey((255, 255, 255))  # remove white background
        self.fox_img = pygame.transform.scale(raw_head, (64, 64))
        self.fox_render_size = 64
        
    
        # Hitbox is smaller than the sprite so it feels fair
        self.hitbox_padding = 18
        self.hitbox_size = self.fox_render_size - (self.hitbox_padding * 2)

        self.fox_x = 100

        self.gravity = 0.35
        self.jump_strength = -7.2

        self.pipe_width = 70
        self.pipe_gap = 160
        self.pipe_speed = 3.5
        self.pipe_delay = 1800

        self.ground_height = 40

        self.reset()

    def reset(self):
        self.fox_y = float(cfg.HEIGHT // 2)
        self.fox_velocity = 0.0
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False
        self.started = False  # wait for first flap before physics start
        self.blueberries_earned = 0
        self.last_reward_score = 0  # tracks last score milestone we rewarded

    def make_pipe(self):
        gap_y = random.randint(130, cfg.HEIGHT - 130 - self.ground_height)
        top_height = gap_y - (self.pipe_gap // 2)
        bottom_y = gap_y + (self.pipe_gap // 2)

        self.pipes.append({
            "x": float(cfg.WIDTH),
            "top_rect": pygame.Rect(cfg.WIDTH, 0, self.pipe_width, top_height),
            "bottom_rect": pygame.Rect(
                cfg.WIDTH, bottom_y,
                self.pipe_width, cfg.HEIGHT - bottom_y - self.ground_height
            ),
            "passed": False
        })

    def get_hitbox(self):
        # Tight hitbox centered on the sprite
        return pygame.Rect(
            self.fox_x + self.hitbox_padding,
            int(self.fox_y) + self.hitbox_padding,
            self.hitbox_size,
            self.hitbox_size
        )

    def flap(self):
        if self.game_over:
            self.reset()
        else:
            self.started = True
            self.fox_velocity = self.jump_strength

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.flap()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.flap()

    def update(self, dt):
        pass

        if self.game_over or not self.started:
            return

        self.fox_velocity += self.gravity
        self.fox_y += self.fox_velocity

        self.pipe_timer += dt
        if self.pipe_timer >= self.pipe_delay:
            self.pipe_timer = 0
            self.make_pipe()

        for pipe in self.pipes:
            pipe["x"] -= self.pipe_speed
            pipe["top_rect"].x = int(pipe["x"])
            pipe["bottom_rect"].x = int(pipe["x"])

            if not pipe["passed"] and pipe["x"] + self.pipe_width < self.fox_x:
                pipe["passed"] = True
                self.score += 1
                if self.score % 10 == 0 and self.score != self.last_reward_score:
                    self.blueberries_earned += 1
                    self.last_reward_score = self.score

        self.pipes = [p for p in self.pipes if p["x"] + self.pipe_width > 0]

        hitbox = self.get_hitbox()

        if hitbox.top <= 0 or hitbox.bottom >= cfg.HEIGHT - self.ground_height:
            self.game_over = True

        for pipe in self.pipes:
            if hitbox.colliderect(pipe["top_rect"]) or hitbox.colliderect(pipe["bottom_rect"]):
                self.game_over = True

    def draw_background(self):
        self.screen.fill((170, 220, 255))
        pygame.draw.rect(self.screen, (100, 180, 100),
                         pygame.Rect(0, cfg.HEIGHT - self.ground_height, cfg.WIDTH, self.ground_height))

    def draw_pipes(self):
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (60, 180, 75), pipe["top_rect"])
            pygame.draw.rect(self.screen, (60, 180, 75), pipe["bottom_rect"])
            # Pipe caps
            top_cap = pygame.Rect(pipe["top_rect"].x - 4, pipe["top_rect"].bottom - 20, self.pipe_width + 8, 20)
            bottom_cap = pygame.Rect(pipe["bottom_rect"].x - 4, pipe["bottom_rect"].y, self.pipe_width + 8, 20)
            pygame.draw.rect(self.screen, (40, 140, 55), top_cap)
            pygame.draw.rect(self.screen, (40, 140, 55), bottom_cap)

    def draw_fox(self):
        self.screen.blit(self.fox_img, (self.fox_x, int(self.fox_y)))

    def draw_ui(self):
        score_text = self.font.render(f"score: {self.score}", True, cfg.BLACK)
        self.screen.blit(score_text, (20, 20))

        esc_text = self.small_font.render("ESC = back to menu", True, cfg.BLACK)
        self.screen.blit(esc_text, (cfg.WIDTH - esc_text.get_width() - 10, 10))

        if self.game_over:
            over_text = self.big_font.render("GAME OVER", True, cfg.BLACK)
            restart_text = self.font.render("space or click to restart", True, cfg.BLACK)
            self.screen.blit(over_text, ((cfg.WIDTH - over_text.get_width()) // 2, 170))
            self.screen.blit(restart_text, ((cfg.WIDTH - restart_text.get_width()) // 2, 230))
            if self.blueberries_earned > 0:
                reward_text = self.font.render(f"+{self.blueberries_earned} blueberry!", True, (70, 100, 220))
                self.screen.blit(reward_text, ((cfg.WIDTH - reward_text.get_width()) // 2, 280))

        # Show a flash message when a reward is just earned
        if not self.game_over and self.score > 0 and self.score == self.last_reward_score:
            flash = self.font.render("+1 blueberry!", True, (70, 100, 220))
            self.screen.blit(flash, ((cfg.WIDTH - flash.get_width()) // 2, 80))
            
        elif not self.started:
            start_text = self.font.render("space or click to start!", True, cfg.BLACK)
            self.screen.blit(start_text, ((cfg.WIDTH - start_text.get_width()) // 2, 180))

        else:
            help_text = self.small_font.render("space or click = flap", True, cfg.BLACK)
            self.screen.blit(help_text, ((cfg.WIDTH - help_text.get_width()) // 2, 20))

    def draw(self):
        self.draw_background()
        self.draw_pipes()
        self.draw_fox()
        self.draw_ui()

    def run(self):
        while True:
            dt = self.clock.tick(cfg.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", self.blueberries_earned
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "exit", self.blueberries_earned
                self.handle_event(event)

            self.update(dt)
            self.draw()
            pygame.display.flip()


def run_flappy_game(screen=None):
    # Reuse the existing screen if passed in, otherwise create one
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Flappy Fox")
    game = FlappyFoxGame(screen)
    return game.run()


if __name__ == "__main__":
    run_flappy_game()