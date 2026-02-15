import pygame
import sys
import config as cfg        # imports config file for ease of project

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

    def update(self,dt):
        self.hunger -= 0.01 * dt
        self.happiness -= 0.005 * dt

# Running parameters
Running = True
clock = pygame.time.Clock()

# Initialize pet class
my_pet = Pet()

while Running:
    # stands for delta time, which is apparently commonly used for stuff like characters state updates
    # FPS = 60
    dt = clock.tick(cfg.FPS) / 1000      #frame rate, /1000 converts time to seconds

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #reads if window closes
            Running = False

    # pet update logic
    my_pet.update(dt)

    # WHITE = (255,255,255)
    screen.fill(cfg.WHITE) # white screen for now
    #Update the display tp show changes
    
    #for character display (template)
    #Pet.draw((how big i wanted to make the character,x , y))


    pygame.display.flip()


# closing pygame and closing the program
pygame.quit()

sys.exit()