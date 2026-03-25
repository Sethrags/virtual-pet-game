import pygame
import sys
import config as cfg        # imports config file for ease of project
from animation_module import Animator # This is for rendering images


#---------------------
# VIRTUAL PET PROJECT
#---------------------
# Main features to work on for now: 
# pet hunger, hapiness and energy systems
# game over systems
# animation sequences
#---------------------


# Initialize Pygame modules
pygame.init()

# Window dimensions (put this on config.py?)
#WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((cfg.WIDTH,cfg.HEIGHT))

# Window Title (Will be changed as we progress)
pygame.display.set_caption("Pet Project")

# main class for pet
class Pet:
    def __init__(self):
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        # dummy code for now
        # the animator will take the png and scale
        # We will need to include some if statements 
        # so we can get the overall logic
        # This is where we put all the possible animations for the pet
        self.animations = {
            "Idle": Animator(cfg.ASSETS_DIR / "spritesheet_idle_animation.png", 48, 48, scale= 6)
            #"Hungry": Animator("Pet_idle_hungry.png",32,32,scale=4),
            #"Eating": Animator("Pet_eating.png", 32, 32, scale =4),
            #"Sleeping": Animator("spritesheet_sleeping_animation.png", 48,48,scale = 6)
        }
        self.state = "Idle" # Set this up as the starting state for the pet
    
    def update(self,dt):
        self.hunger -= 0.00001 * dt
        self.happiness -= 0.000005 * dt
        self.animations[self.state].update(dt) # animating the pet

    def draw(self, screen):
        fox_half_size = (48 * 6) // 2 # If you change the scale, remember to change this too
        pos_x = (cfg.WIDTH // 2) - fox_half_size
        pos_y = (cfg.HEIGHT // 2) - fox_half_size
        self.animations[self.state].draw(screen,pos_x,pos_y)

    def change_state(self,new_state):
        if self.state != new_state:
            self.state = new_state
            self.animations[self.state].current_frame = 0
            self.animations[self.state].timer=0

#----------------------------------------#
# Running parameters
Running = True
clock = pygame.time.Clock()

# Initialize pet class
my_pet = Pet()

while Running:
    # stands for delta time, which is apparently commonly used for stuff like characters state updates
    # FPS = 60
    dt = clock.tick(cfg.FPS)    #frame rate

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #reads if window closes
            Running = False

    # pet update logic
    my_pet.update(dt)
    #print(f"Happ: {my_pet.happiness}")

    # WHITE = (255,255,255)
    screen.fill(cfg.WHITE) # white screen for now
    #Update the display tp show changes
    
    #for character display (template)
    my_pet.draw(screen)
    pygame.display.flip()


# closing pygame and closing the program
pygame.quit()

sys.exit()