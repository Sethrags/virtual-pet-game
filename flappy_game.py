# Filename: flappy_game.py
# Author: Seth
# Description: This file implements a simple Flappy Bird-style mini-game called "Flappy Fox" using Pygame.
# The game features a fox that the player controls by making it flap to avoid oncoming pipes.
# The player earns blueberries as rewards for reaching score milestones.
import random
import pygame
import config as cfg

# FlappyFoxGame class
# This class encapsulates all the functionality of the Flappy Fox game. It manages the game state, including
# the position and movement of the fox, the generation and movement of pipes, collision detection, scoring, and 
# rendering the game elements on the screen. The class provides methods for handling user input (flapping),updating 
# the game state based on physics and collisions, drawing the game elements (background, pipes, fox, UI), and running 
# the main game loop. The game loop processes events, updates the game state, and renders the graphics at a consistent frame rate.
class FlappyFoxGame:

    # Initializer for the FlappyFoxGame class. 
    # It sets up the game screen, loads assets, and initializes game variables.
    def __init__(self, screen):
        # Initialize the game screen and clock for managing frame rate
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Load fonts for rendering text in the game, using the Grand9K Pixel font from the assets directory.
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

        # Initial position of the fox on the x-axis (fixed) and y-axis (variable)
        self.fox_x = 100

        # Game physics and pipe settings
        self.gravity = 0.35
        self.jump_strength = -7.2

        # Pipe settings: width, gap between top and bottom, speed of movement, and delay between new pipes
        self.pipe_width = 70
        self.pipe_gap = 160
        self.pipe_speed = 3.5
        self.pipe_delay = 1800
        self.ground_height = 40

        # Initialize the game state by calling the reset method
        self.reset()

    # reset
    # This method resets the game state to its initial conditions. It sets the fox's vertical position and velocity,
    # clears the list of pipes, resets the pipe timer, score, game over status, and
    def reset(self):
        # Set the fox's vertical position to the middle of the screen and reset its velocity to 0. 
        # Clear the list of pipes, reset the pipe timer, score, game over status, and other related 
        # variables to their initial values.
        self.fox_y = float(cfg.HEIGHT // 2)
        self.fox_velocity = 0.0
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.game_over = False
        self.started = False  # wait for first flap before physics start
        self.blueberries_earned = 0
        self.last_reward_score = 0  # tracks last score milestone we rewarded

    # make_pipe
    # This method generates a new pipe obstacle for the game. It randomly determines the vertical position of the 
    # gap between the top and bottom pipes, and creates rectangles for the top and bottom pipes based on the calculated positions.
    def make_pipe(self):
        # Randomly determine the vertical position of the gap between the top and bottom pipes, 
        # ensuring it stays within the screen bounds.
        gap_y = random.randint(130, cfg.HEIGHT - 130 - self.ground_height)
        top_height = gap_y - (self.pipe_gap // 2)
        bottom_y = gap_y + (self.pipe_gap // 2)

        # Create rectangles for the top and bottom pipes based on the calculated positions and add them to the list of pipes.
        self.pipes.append({
            "x": float(cfg.WIDTH),
            "top_rect": pygame.Rect(cfg.WIDTH, 0, self.pipe_width, top_height),
            "bottom_rect": pygame.Rect(
                cfg.WIDTH, bottom_y,
                self.pipe_width, cfg.HEIGHT - bottom_y - self.ground_height
            ),
            "passed": False
        })

    # get_hitbox
    # This method calculates and returns the hitbox for the fox character. 
    # The hitbox is a smaller rectangle centered on the fox sprite, which is used for collision detection with pipes and the ground.
    def get_hitbox(self):
        # Tight hitbox centered on the sprite
        return pygame.Rect(
            self.fox_x + self.hitbox_padding,
            int(self.fox_y) + self.hitbox_padding,
            self.hitbox_size,
            self.hitbox_size
        )

    # flap
    # This method handles the action of the fox flapping. If the game is over, it resets the game state.
    def flap(self):
        # If the game is over, reset the game state to start a new game. Otherwise, set the started flag to True and
        # give the fox an upward velocity to simulate the flap action.
        if self.game_over:
            self.reset()
        else:
            self.started = True
            self.fox_velocity = self.jump_strength

    # handle_event
    # This method processes user input events. Listens for key presses or mouse clicks to trigger the flap action.
    def handle_event(self, event):
        # Listen spacebarto trigger the flap action.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.flap()
        # Also allow mouse clicks to flap for accessibility and ease of play on different devices
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.flap()

    # update
    # This method updates the game state based on the passage of time (delta time) and the current conditions of the game.
    # It applies gravity to the fox's velocity, moves the fox, generates new pipes at intervals, moves existing pipes,
    # checks for collisions with pipes and the ground, and updates the score and rewards.
    def update(self, dt):
        pass

        # If the game is over or hasn't started yet, skip the update logic to keep the fox stationary and not generate pipes.
        if self.game_over or not self.started:
            return

        # Apply gravity to the fox's velocity and update its vertical position based on the velocity.
        self.fox_velocity += self.gravity
        self.fox_y += self.fox_velocity

        # Update the pipe timer and generate new pipes at intervals defined by self.pipe_delay. 
        self.pipe_timer += dt
        if self.pipe_timer >= self.pipe_delay:
            self.pipe_timer = 0
            self.make_pipe()

        # Move existing pipes to the left and check if the fox has passed them to update the score.
        for pipe in self.pipes:
            pipe["x"] -= self.pipe_speed
            pipe["top_rect"].x = int(pipe["x"])
            pipe["bottom_rect"].x = int(pipe["x"])

            # Check if the fox has passed the pipe and update the score accordingly.
            if not pipe["passed"] and pipe["x"] + self.pipe_width < self.fox_x:
                pipe["passed"] = True
                self.score += 1
                if self.score % 10 == 0 and self.score != self.last_reward_score:
                    self.blueberries_earned += 1
                    self.last_reward_score = self.score

        # Remove pipes that have moved off the left side of the screen to free up resources.
        self.pipes = [p for p in self.pipes if p["x"] + self.pipe_width > 0]

        # Check for collisions with the ground and pipes. If a collision is detected, set the game over status to True.
        hitbox = self.get_hitbox()
        if hitbox.top <= 0 or hitbox.bottom >= cfg.HEIGHT - self.ground_height:
            self.game_over = True
        for pipe in self.pipes:
            if hitbox.colliderect(pipe["top_rect"]) or hitbox.colliderect(pipe["bottom_rect"]):
                self.game_over = True

    # draw_background
    # This method draws the background of the game, including the sky and the ground.
    def draw_background(self):
        self.screen.fill((170, 220, 255))
        pygame.draw.rect(self.screen, (100, 180, 100),
                         pygame.Rect(0, cfg.HEIGHT - self.ground_height, cfg.WIDTH, self.ground_height))

    # draw_pipes
    # This method draws the pipes on the screen. It iterates through the list of pipes and draws the top 
    # and bottom rectangles for each pipe, as well as decorative caps on the pipes to make them visually distinct and appealing.
    def draw_pipes(self):
        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (60, 180, 75), pipe["top_rect"])
            pygame.draw.rect(self.screen, (60, 180, 75), pipe["bottom_rect"])
            # Pipe caps
            top_cap = pygame.Rect(pipe["top_rect"].x - 4, pipe["top_rect"].bottom - 20, self.pipe_width + 8, 20)
            bottom_cap = pygame.Rect(pipe["bottom_rect"].x - 4, pipe["bottom_rect"].y, self.pipe_width + 8, 20)
            pygame.draw.rect(self.screen, (40, 140, 55), top_cap)
            pygame.draw.rect(self.screen, (40, 140, 55), bottom_cap)

    # draw_fox
    # This method draws the fox character on the screen at its current position. 
    # It uses the blit method to render the fox image onto the screen.
    def draw_fox(self):
        self.screen.blit(self.fox_img, (self.fox_x, int(self.fox_y)))

    # draw_ui
    # This method draws the user interface elements on the screen, including the score, instructions, and game over messages.
    # It displays the current score in the top left corner, instructions for controls, and if the game is over, 
    # it shows a game over message and the rewards earned. It also shows a flash message when a reward is just earned.
    def draw_ui(self):
        score_text = self.font.render(f"score: {self.score}", True, cfg.BLACK)
        self.screen.blit(score_text, (20, 20))

        esc_text = self.small_font.render("ESC = back to menu", True, cfg.BLACK)
        self.screen.blit(esc_text, (cfg.WIDTH - esc_text.get_width() - 10, 10))

         # If the game is over, display a game over message and the rewards earned. 
         # If the game hasn't started yet, show instructions to start.
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

    # draw
    # This method draws all the game elements on the screen by calling the respective draw methods for the background, pipes, fox, and UI.
    # It ensures that all visual elements are rendered in the correct order to create the complete game scene.
    def draw(self):
        self.draw_background()
        self.draw_pipes()
        self.draw_fox()
        self.draw_ui()

    # run
    # This method contains the main game loop that keeps the game running. It processes user input events, updates the game state,
    # and renders the game elements on the screen at a consistent frame rate. The loop continues until the player chooses to exit 
    # the game, at which point it returns the rewards earned based on the player's score.
    def run(self):
        while True:
            dt = self.clock.tick(cfg.FPS)

            # Process events for quitting the game or returning to the menu. 
            # If the player closes the window or presses the ESC key,
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", self.blueberries_earned
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "exit", self.blueberries_earned
                self.handle_event(event)

            # Update the game state based on the passage of time and current conditions,
            # then draw all game elements on the screen and update the display.
            self.update(dt)
            self.draw()
            pygame.display.flip()

# run_flappy_game
# This function initializes and runs the Flappy Fox game. It can take an optional screen parameter to reuse an 
# existing Pygame screen, or it will create a new one if not provided. It sets the window caption and creates an 
# instance of the FlappyFoxGame class, then calls the run method to start the game loop.
def run_flappy_game(screen=None):
    # Reuse the existing screen if passed in, otherwise create one
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Flappy Fox")
    game = FlappyFoxGame(screen)
    return game.run()

# Main block to run the Flappy Fox game when this file is executed directly.
if __name__ == "__main__":
    run_flappy_game()