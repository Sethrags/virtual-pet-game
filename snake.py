# Filename: snake.py
# Author: Evan
# Description: This file implements a simple Snake mini-game that can be played within the Tamagotchi game.
# The game features a snake that the player can control using the W A S D or arrow keys to eat food and grow longer.
# The game includes a start screen, a main game loop, and a game over screen that displays the player's score and
# rewards earned based on their performance.
import pygame
import random
import config as cfg

CELL = 20 # Size of each cell in the grid (20x20 pixels)

# Colors used in the game
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# run_snake_game
# This function runs the Snake mini-game. It initializes the game state, handles user input,
# updates the game logic, and renders the game on the screen. The function returns a dictionary 
# of rewards earned based on the player's score when the game ends.
def run_snake_game(screen):
    # Initialize Pygame and set up the game window, clock, and fonts
    clock = pygame.time.Clock()
    font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 24)
    big_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 48)

    # Snake initial settings
    snake_pos = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"

    #spawn food in a random position that is not on the snake
    def spawn_food():
        while True:
            pos = [
                random.randrange(0, cfg.WIDTH // CELL) * CELL,
                random.randrange(0, cfg.HEIGHT // CELL) * CELL
            ]
            if pos not in snake_pos:
                return pos

    food_pos = spawn_food() # Initial food position
    score = 0 # Initial score

    #draw_snake
    # This function draws the snake on the screen. It iterates through each segment of the snake's position 
    # and draws a rectangle for each segment using the pygame.draw.rect method. The snake is colored orange and each segment 
    # is drawn as a cell of size defined by the CELL constant.
    def draw_snake():
        for block in snake_pos:
            pygame.draw.rect(screen, ORANGE, pygame.Rect(block[0], block[1], CELL, CELL))

    # draw_food
    # This function draws the food on the screen. It uses the pygame.draw.rect method to draw a red rectangle at the food's position,
    # which is defined by the food_pos variable. The food is also drawn as a cell of size defined by the CELL constant.
    def draw_food():
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL, CELL))

    # show_score
    # This function displays the player's current score on the screen. It renders the score text using
    # the defined font and blits it onto the screen at a fixed position (10, 10). The score is displayed in white color.
    def show_score():
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

    # Start Screen loop
    waiting = True
    while waiting:

        # Handle events for the start screen. The game will start when the player clicks or presses any key, 
        # and it will return to the menu if the player presses the ESC key.
        for event in pygame.event.get():
            # If the player closes the window, return None to exit the game
            if event.type == pygame.QUIT:
                return None
            # If the player clicks or presses any key, start the game by setting waiting to False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # start the game
            # If the player presses the ESC key, return None to go back to the menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None  # return to menu

        # Main game loop will run until the player collides with the wall or itself. 
        # It handles user input for controlling the snake's direction,
        screen.fill(BLACK)
        title = big_font.render("SNAKE", True, ORANGE)
        move1 = font.render("Use W A S D or Arrow Keys to Move", True, WHITE)
        move2 = font.render("Press ESC to Return to Menu", True, WHITE)
        prompt = font.render("Click or Press Any Key to Start", True, ORANGE)

        # Blit the title and instructions onto the screen, centering them horizontally and positioning them vertically with some spacing.
        screen.blit(title, (cfg.WIDTH//2 - title.get_width()//2, cfg.HEIGHT//2 - 120))
        screen.blit(move1, (cfg.WIDTH//2 - move1.get_width()//2, cfg.HEIGHT//2 - 40))
        screen.blit(move2, (cfg.WIDTH//2 - move2.get_width()//2, cfg.HEIGHT//2))
        screen.blit(prompt, (cfg.WIDTH//2 - prompt.get_width()//2, cfg.HEIGHT//2 + 80))

        # Update the display and tick the clock to control the frame rate of the start screen animation.
        pygame.display.update()
        clock.tick(30)

    # Main Game Loop
    running = True
    while running:
        # Handle events for the main game loop. 
        # The player can control the snake's direction using W A S D or arrow keys, and can return to the menu by pressing the ESC key.
        for event in pygame.event.get():
            # If the player closes the window, return None to exit the game
            if event.type == pygame.QUIT:
                return None
            # If the player presses the ESC key, return None to go back to the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None  # return to pet game menu

                # Handle direction changes based on user input, ensuring that the snake cannot reverse direction directly 
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

        # Update the snake's head position based on the current direction. 
        # The snake moves by adding a new head in the direction of movement and removing the tail segment unless it has just eaten food.
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

        # Check if the snake has eaten the food. 
        # If the new head position matches the food position, increment the score and spawn new food.
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

        # Update the display and tick the clock to control the frame rate of the game loop.
        pygame.display.update()
        clock.tick(10)

    # rewards
    rewards = {
        "Blueberry": score // 5,
        "Raspberry": score // 10,
        "Cookie": 1 if score >= 20 else 0
    }

    # Game Over Screen loop
    summary_running = True
    while summary_running:
        # Handle events for the game over screen. 
        # The player can exit the game by closing the window or can return to the menu by pressing any key or clicking.
        for event in pygame.event.get():
            # If the player closes the window, return rewards to exit the game
            if event.type == pygame.QUIT:
                return rewards
            # If the player clicks or presses any key, exit the game over screen loop and return rewards to go back to the menu
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                summary_running = False

        # Draw the game over screen with the player's score and rewards earned.
        screen.fill(BLACK)
        title = big_font.render(f"GAME OVER", True, ORANGE)
        reward_title = font.render("Rewards Earned:", True, WHITE)

        # Render the rewards earned based on the player's score, displaying the number of blueberries, raspberries, and cookies earned.
        b_txt = font.render(f"Blueberries: {rewards['Blueberry']}", True, WHITE)
        r_txt = font.render(f"Raspberries: {rewards['Raspberry']}", True, WHITE)
        c_txt = font.render(f"Cookies: {rewards['Cookie']}", True, WHITE)

        prompt = font.render("Press Any Key to Continue", True, ORANGE)
        # Blit the game over title, rewards summary, and prompt onto the screen, 
        # centering them horizontally and positioning them vertically with some spacing.
        screen.blit(title, (cfg.WIDTH//2 - title.get_width()//2, 150))
        screen.blit(reward_title, (cfg.WIDTH//2 - reward_title.get_width()//2, 230))
        screen.blit(b_txt, (cfg.WIDTH//2 - b_txt.get_width()//2, 290))
        screen.blit(r_txt, (cfg.WIDTH//2 - r_txt.get_width()//2, 330))
        screen.blit(c_txt, (cfg.WIDTH//2 - c_txt.get_width()//2, 370))
        screen.blit(prompt, (cfg.WIDTH//2 - prompt.get_width()//2, 450))
        
        # Update the display and tick the clock to control the frame rate of the game over screen animation.
        pygame.display.update() 
        clock.tick(30) 

    return rewards # Return the rewards earned based on the player's score when the game ends
