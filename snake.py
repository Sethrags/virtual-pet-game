import pygame
import random
import config as cfg

CELL = 20

# Colors
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def run_snake_game(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 24)
    big_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 48)

    # Snake initial settings
    snake_pos = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"

    # Food spawn function that avoids the snake
    def spawn_food():
        while True:
            pos = [
                random.randrange(0, cfg.WIDTH // CELL) * CELL,
                random.randrange(0, cfg.HEIGHT // CELL) * CELL
            ]
            if pos not in snake_pos:
                return pos

    food_pos = spawn_food()
    score = 0

    def draw_snake():
        for block in snake_pos:
            pygame.draw.rect(screen, ORANGE, pygame.Rect(block[0], block[1], CELL, CELL))

    def draw_food():
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL, CELL))

    def show_score():
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

    # -------------------------
    # START SCREEN
    # -------------------------
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # start the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None  # return to menu

        screen.fill(BLACK)
        title = big_font.render("SNAKE", True, ORANGE)
        move1 = font.render("Use W A S D or Arrow Keys to Move", True, WHITE)
        move2 = font.render("Press ESC to Return to Menu", True, WHITE)
        prompt = font.render("Click or Press Any Key to Start", True, ORANGE)

        screen.blit(title, (cfg.WIDTH//2 - title.get_width()//2, cfg.HEIGHT//2 - 120))
        screen.blit(move1, (cfg.WIDTH//2 - move1.get_width()//2, cfg.HEIGHT//2 - 40))
        screen.blit(move2, (cfg.WIDTH//2 - move2.get_width()//2, cfg.HEIGHT//2))
        screen.blit(prompt, (cfg.WIDTH//2 - prompt.get_width()//2, cfg.HEIGHT//2 + 80))

        pygame.display.update()
        clock.tick(30)

    # -------------------------
    # MAIN GAME LOOP
    # -------------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None  # return to pet game menu

                if (event.key in (pygame.K_UP, pygame.K_w)) and direction != "DOWN":
                    direction = "UP"
                elif (event.key in (pygame.K_DOWN, pygame.K_s)) and direction != "UP":
                    direction = "DOWN"
                elif (event.key in (pygame.K_LEFT, pygame.K_a)) and direction != "RIGHT":
                    direction = "LEFT"
                elif (event.key in (pygame.K_RIGHT, pygame.K_d)) and direction != "LEFT":
                    direction = "RIGHT"

        # Move snake
        x, y = snake_pos[0]

        if direction == "UP":
            y -= CELL
        elif direction == "DOWN":
            y += CELL
        elif direction == "LEFT":
            x -= CELL
        elif direction == "RIGHT":
            x += CELL

        new_head = [x, y]
        snake_pos.insert(0, new_head)

        # Food collision
        if new_head == food_pos:
            score += 1
            food_pos = spawn_food()
        else:
            snake_pos.pop()

        # Wall collision
        if x < 0 or x >= cfg.WIDTH or y < 0 or y >= cfg.HEIGHT:
            break

        # Self collision
        if new_head in snake_pos[1:]:
            break

        # Draw everything
        screen.fill(BLACK)
        draw_snake()
        draw_food()
        show_score()

        pygame.display.update()
        clock.tick(10)

    # rewards
    rewards = {
        "Blueberry": score // 5,
        "Raspberry": score // 10,
        "Cookie": 1 if score >= 20 else 0
    }

    summary_running = True
    while summary_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return rewards
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                summary_running = False

        screen.fill(BLACK)

        title = big_font.render(f"GAME OVER", True, ORANGE)
        reward_title = font.render("Rewards Earned:", True, WHITE)

        b_txt = font.render(f"Blueberries: {rewards['Blueberry']}", True, WHITE)
        r_txt = font.render(f"Raspberries: {rewards['Raspberry']}", True, WHITE)
        c_txt = font.render(f"Cookies: {rewards['Cookie']}", True, WHITE)

        prompt = font.render("Press Any Key to Continue", True, ORANGE)

        screen.blit(title, (cfg.WIDTH//2 - title.get_width()//2, 150))
        screen.blit(reward_title, (cfg.WIDTH//2 - reward_title.get_width()//2, 230))

        screen.blit(b_txt, (cfg.WIDTH//2 - b_txt.get_width()//2, 290))
        screen.blit(r_txt, (cfg.WIDTH//2 - r_txt.get_width()//2, 330))
        screen.blit(c_txt, (cfg.WIDTH//2 - c_txt.get_width()//2, 370))

        screen.blit(prompt, (cfg.WIDTH//2 - prompt.get_width()//2, 450))
        
        pygame.display.update()
        clock.tick(30)

    return rewards
