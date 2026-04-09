import pygame
import sys
import config as cfg        # imports config file for ease of project
from animation_module import Animator # This is for rendering images
from weatherapp import get_weather # this is the code for the weather application - Evan


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

# This code is for the custom font (pixelated font)
custom_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 32) # We will test out the font size

# Window dimensions (put this on config.py?)
#WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((cfg.WIDTH,cfg.HEIGHT))

# Window Title (Will be changed as we progress)
pygame.display.set_caption("Pet Project")

# --- FEED, SLEEP, GAME BUTTONS ---
btn_width = 140
btn_height = 60
btn_y_pos = cfg.HEIGHT - 80
feed_button = pygame.Rect(20, btn_y_pos, btn_width, btn_height)
sleep_button = pygame.Rect(180, btn_y_pos,btn_width, btn_height)
game_button = pygame.Rect(340, btn_y_pos, btn_width, btn_height)

settings_open = False # Toggle for the settings menu

# --- SETTINGS BUTTON and BUTTON ICON-- 
# For the raw asset image
raw_icon = pygame.image.load(cfg.ASSETS_DIR / "settings_button.png").convert()
raw_icon.set_colorkey(cfg.WHITE) # Don't want White background from the gear icon
gear_area = raw_icon.get_bounding_rect()# Finding the tightest box around gear
# For the icon surface and all the other stuff for filling
cropped_icon = pygame.Surface(gear_area.size)
cropped_icon.fill(cfg.WHITE)
cropped_icon.set_colorkey(cfg.WHITE)
cropped_icon.blit(raw_icon,(0,0),gear_area)
#settings icon and button
settings_icon = pygame.transform.scale_by(cropped_icon, 3.5)
settings_btn = settings_icon.get_rect(topright=(cfg.WIDTH - 20, 20))

# --- Button colors ---
BUTTON_COLOR = (100,100,100)
BUTTON_HOVER = (150,150,150)

# --- BACK BUTTON ICON ---
# Will also need to set the settings for a back button for exiting feeding and such
# Raw asset (similar to settings button)
raw_back_icon = pygame.image.load(cfg.ASSETS_DIR / "back_button_icon.png").convert()
raw_back_icon.set_colorkey(cfg.WHITE)
# Find tightest box around the arrow icon
back_icon_area = raw_back_icon.get_bounding_rect()

cropped_back_icon = pygame.Surface(back_icon_area.size)
cropped_back_icon.fill(cfg.WHITE)
cropped_back_icon.set_colorkey(cfg.WHITE)
cropped_back_icon.blit(raw_back_icon, (0,0), back_icon_area)

back_icon = pygame.transform.scale_by(cropped_back_icon, 4)
back_btn_rect = back_icon.get_rect(topleft=(20,20))



# main class for pet
class Pet:
    def __init__(self):
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        # dummy code for now
        # This is where we put all the possible animations for the pet
        self.animations = {
            "Idle": Animator(cfg.ASSETS_DIR / "spritesheet_idle_animation.png", 48, 48, scale= 6)
            #"Hungry": Animator("Pet_idle_hungry.png",32,32,scale=4),
            #"Eating": Animator("Pet_eating.png", 32, 32, scale =4),
            #"Sleeping": Animator("spritesheet_sleeping_animation.png", 48,48,scale = 6)
        }
        self.state = "Idle" # Set this up as the starting state for the pet
    
    def update(self,dt): # let me know if you want me to add something onto this for pet status based on weather
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

    def feed(self):
        self.hunger = min(100,self.hunger + 15)
        print(f"Feeding: Hunger = {int(self.hunger)}")
    
    def sleep(self):
        raise NotImplementedError

    def play_game():
        raise NotImplementedError

    '''def apply_weather_effects(self, weather):
        if weather is None:
            return
        
        category = weather[category]

        if category == "cold":
            self.energy -= 0.005 # test
        elif category == "hot":
            self.hunger -= 0.005 # test
        elif category == "temperate":
            self.happiness += 0.002 # test

font = pygame.font.Sysfont(None, 32)
user_text = ""
asking_location = True
weather = None'''

# We need a food item class for the feeding implementation
class FoodItem:
    # Initializer for the food item, makes it easier for many object implementations in case we need to add more
    def __init__(self,name,img_path,x,y):
        self.name = name
        # Load and scale image
        raw_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale_by(raw_image, 3)
        self.image.set_colorkey(cfg.WHITE)
        #self.image.set_colorkey(cfg.WHITE)
        #self.rect = self.image.get_rect(center=(x,y))
        #self.original_pos = (x, y)
        #self.dragging = False
        box_rect = self.image.get_bounding_rect()
        self.rect = self.image.get_rect()

        self.rect.centerx = x - (box_rect.centerx - (self.image.get_width() // 2))
        self.rect.centery = y - (box_rect.centery - (self.image.get_height() // 2))

        self.original_pos = self.rect.center
        self.dragging = False

    def handle_events(self,event,mouse_pos,pet_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False

                # Since we lifted the button we need 
                # to check whether it was done by the pet's mouth for feeding
                if self.rect.colliderect(pet_rect):
                    my_pet.feed() # This triggers the feeding logic
                self.rect.center = self.original_pos
    def update(self,mouse_pos):
        if self.dragging:
            self.rect.center = mouse_pos
    def draw(self,screen):
        screen.blit(self.image, self.rect)


#----------------------------------------#
# Running parameters
Running = True
clock = pygame.time.Clock()
scene = "MAIN" # for switching scenes
my_pet = Pet() # Initialize pet

# Initialize food items
slot1_x = cfg.WIDTH // 6
slot2_x = (cfg.WIDTH // 6) * 3
slot3_x = (cfg.WIDTH // 6) * 5
slot_y = cfg.HEIGHT - 80

foods = [
    FoodItem("Blueberry", cfg.ASSETS_DIR / "blueberry.png", slot1_x, slot_y),
    FoodItem("Raspberry", cfg.ASSETS_DIR / "raspberry.png", slot2_x, slot_y),
    FoodItem("Cookie", cfg.ASSETS_DIR / "cookie.png", slot3_x, slot_y)
]

while Running:
    dt = clock.tick(cfg.FPS)    #frame rate/delta time
    mouse_pos = pygame.mouse.get_pos()

    # Mouth Hitbox (Feeding)
    pet_rect = pygame.Rect(cfg.WIDTH // 2 - 40, cfg.HEIGHT // 2 - 40, 80, 80)
    
    # Event Handler
    for event in pygame.event.get():
        # Quit button
        if event.type == pygame.QUIT:
            Running = False

        # Scene switch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if scene == "MAIN":
                if settings_btn.collidepoint(mouse_pos):
                    settings_open = not settings_open
                if not settings_open and feed_button.collidepoint(mouse_pos):
                    scene = "FEED"

            elif scene == "FEED":
                if back_btn_rect.collidepoint(mouse_pos): 
                    scene = "MAIN"
        
        # Dragging the food event
        if scene == "FEED":
            for food in foods:
                food.handle_events(event, mouse_pos, pet_rect)

    screen.fill(cfg.WHITE)

    if scene == "MAIN":
        # Pet Display logic for main
        my_pet.update(dt)
        my_pet.draw(screen)

        # ---Drawing section---
        if settings_open:
            overlay = pygame.Surface((cfg.WIDTH,cfg.HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))

            s_text = custom_font.render("SETTINGS",True,cfg.WHITE)
            back_text = custom_font.render("Click SETTINGS Box to close",True,cfg.WHITE)
            screen.blit(s_text, (cfg.WIDTH//2 - 100, 150))
            screen.blit(back_text,(cfg.WIDTH//2 - 150, 250))

        else:
            # Button Drawing Implementation
            for rect, label in [(feed_button,"FEED"),(sleep_button, "SLEEP"),(game_button,"GAME")]:
                # Change the color if the mouse is hovering
                color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(screen,color,rect)

                # Box outline (black)
                pygame.draw.rect(screen, cfg.BLACK,rect, 4)
                # Custom font implementation
                txt_surface = custom_font.render(label,True,cfg.WHITE)
                # Centering the text in the button
                screen.blit(txt_surface,(rect.x + 15, rect.y + 12))
    
            # Drawing settings button for this specific setup (this will always display it)
        if settings_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen,BUTTON_HOVER,settings_btn,border_radius=8)
        screen.blit(settings_icon,settings_btn)

    elif scene == "FEED":
        my_pet.update(dt)
        screen.blit(back_icon,back_btn_rect)
        my_pet.draw(screen)

        for i in range(3):
            slot_width = 80
            slot_height = 80

            x_pos = ((cfg.WIDTH // 6) * (1 + 2 * i)) - (slot_width // 2)
            y_pos = (cfg.HEIGHT - 80) - (slot_height // 2)

            slot_rect = pygame.Rect(x_pos,y_pos,slot_width,slot_height)

            # Displaying the light gray box for food slots
            pygame.draw.rect(screen, (220,220,220),slot_rect,border_radius=10)
            pygame.draw.rect(screen, cfg.BLACK, slot_rect, 2, border_radius=10)

        if back_btn_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen,BUTTON_HOVER,back_btn_rect,border_radius=8)
        screen.blit(back_icon,back_btn_rect)
        
        for food in foods:
            food.update(mouse_pos)
            food.draw(screen)
# this goes with the other weather comment above
        '''if asking_location:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    weather = get_weather(user_text)
                    asking_location = False
                elif event.key == pygame.K_BACKSPACE:
                    user.text = user_text[:-1]
                else:
                    user_text += event.unicode
        
    if asking_location:
        screen.fill((255,255,255))
        prompt = font.render("Enter city", True (0,0,0))
        text_surface = font.render(user_text, True, (0,0,0))

        screen.blit(prompt, (20, 20))
        screen.blit(text_surface, (20, 60))

        pygame.display.flip()
        continue'''
    
    # WHITE = (255,255,255)
    #screen.fill(cfg.WHITE) # white screen for now
    #Update the display tp show changes

    #for character display (template)
    #my_pet.draw(screen)
    pygame.display.flip()


# closing pygame and closing the program
pygame.quit()

sys.exit()