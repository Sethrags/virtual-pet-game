import pygame
import sys
import random
import config as cfg        # imports config file for ease of project
from animation_module import Animator # This is for rendering images
from weatherapp import get_weather # this is the code for the weather application - Evan
from login import run_login_screen #login code import
from flappy_game import run_flappy_game #flappybird Game import
import snake
from lightDatabase import ensure_user_exists, load_pet_data, save_pet_data # light database import for saving/loading pet stats and inventory

def pygame_text_input(prompt="Enter text:", max_length=20):
    input_text = ""
    font = pygame.font.Font(None, 36)

    # Create a semi-transparent overlay
    overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    input_box = pygame.Rect(cfg.WIDTH//2 - 150, cfg.HEIGHT//2, 300, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_pet_data(username, my_pet)
                print("Pet data saved. Exiting game.")
                print("Final Stats - Hunger: {}, Happiness: {}, Energy: {}".format(int(my_pet.hunger), int(my_pet.happiness), int(my_pet.energy)))
                print("Final Inventory - Blueberry: {}, Raspberry: {}, Cookie: {}".format(my_pet.inventory['Blueberry'], my_pet.inventory['Raspberry'], my_pet.inventory['Cookie']))    
            
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                elif len(input_text) < max_length:
                    input_text += event.unicode

        # Draw overlay
        screen.blit(overlay, (0, 0))

        # Draw prompt
        prompt_surf = font.render(prompt, True, cfg.WHITE)
        screen.blit(prompt_surf, (cfg.WIDTH//2 - prompt_surf.get_width()//2,
                                  cfg.HEIGHT//2 - 60))

        # Draw input box
        pygame.draw.rect(screen, cfg.WHITE, input_box, 2)

        # Draw text
        text_surf = font.render(input_text, True, cfg.WHITE)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        pygame.display.flip()

#---------------------
# VIRTUAL PET PROJECT
#---------------------
# Main features to work on for now: 
# pet hunger, hapiness and energy systems
# game over systems
# animation sequences
#---------------------

# Window dimensions (put this on config.py?)
screen = pygame.display.set_mode((cfg.WIDTH,cfg.HEIGHT))

# This will be used for a night overlay in the window
night_overlay = pygame.Surface((cfg.WIDTH,cfg.HEIGHT))
night_overlay.set_alpha(120) # This is the brightness adjustment
night_overlay.fill((10,10,40))

# This class is used for the main pet
class Pet:
    def __init__(self):
        self.hunger = 100
        self.happiness = 100
        self.energy = 100

        # This line of code is going to be used for the implementation
        # of a food inventory system
        self.inventory = {
            "Blueberry": 7,
            "Raspberry": 5,
            "Cookie": 3
        }

        # This is where we put all the possible animations for the pet
        self.animations = {
            "Idle": Animator(cfg.ASSETS_DIR / "spritesheet_idle_animation.png", 48, 48, scale= 6),
            "Hungry": Animator(cfg.ASSETS_DIR / "spritesheet_idle_sad_animation.png",48, 48, scale = 6),
            "Tired": Animator(cfg.ASSETS_DIR / "spritesheet_tired_animation.png",48, 48, scale = 6),
            "Sad_Tired": Animator(cfg.ASSETS_DIR / "spritesheet_tired_sad_animation.png",48, 48, scale = 6),
            "Eating": Animator(cfg.ASSETS_DIR / "spritesheet_feed_animation.png", 48, 48, scale =6),
            "Sleeping": Animator(cfg.ASSETS_DIR / "spritesheet_sleeping_animation.png", 48,48,scale = 6)
        }
        self.state = "Idle" # Set this up as the starting state for the pet
    
    def update(self,dt): 
        # Speed types
        test_speed = 0.001
        hunger_speed_var = 0.00001
        energy_speed_var = 0.00008
        # Variables for testing use only
        hunger_speed = test_speed
        energy_speed = test_speed

        # True pet stat speed
        #hunger_speed = hunger_speed_var
        #energy_speed = energy_speed_var

        # -- Hunger Logic -- 
        self.hunger -= hunger_speed *dt
        self.hunger = max(0,min(100.5,self.hunger))

        # -- Energy Logic --
        if self.state == "Sleeping":
            self.energy += energy_speed * dt
        else:
            self.energy -= energy_speed * dt
        self.energy = max(0, min(100.5,self.energy))

        # --- ANIMATION CHANGE STATES LOGIC FOR SAD ---
        # When the pet sleeps, it's doesnt display sad animation
        if self.state not in ["Sleeping", "Eating"]:
            is_hungry = self.hunger < 15
            is_tired = self.energy < 15

            # Both conditions (hungry and tired)
            if is_hungry and is_tired:
                self.change_state("Sad_Tired")

            elif is_hungry:
                self.change_state("Hungry")
            
            elif is_tired:
                self.change_state("Tired")

            else:
                self.change_state("Idle")


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

    def feed(self, food_name):
        # Food values for different foods
        food_values = {
            "Blueberry": 5,
            "Raspberry": 10,
            "Cookie": 25
        }
        # This gets the value of the food, if not found, then 5 is the default
        value = food_values.get(food_name, 5)

        # Increase hunger
        self.hunger = min(100.5, self.hunger + value)

        # for testing: seeing in the console food values
        print(f"Fed {food_name}: Hunger = {int(self.hunger)}")
        eatingSound.play() # Play eating sound effect when feeding

    def sleep(self):
        if self.state == "Sleeping":
            self.change_state("Idle")
            print("Pet woke up!")
        else:
            self.change_state("Sleeping")
            print("Sleeping...")

    def play_game():
        raise NotImplementedError
    
    # Apply effects to pet pased on current weather if location present
    def apply_weather_effects(self, category):
        if category == "cold":
            self.energy = max(0, self.energy - 0.02)
        elif category == "hot":
            self.hunger = max(0, self.hunger - 0.02)
        elif category == "temperate":
            self.happiness = min(100, self.happiness + 0.01)


# We need a food item class for the feeding implementation
class FoodItem:
    # Initializer for the food item, makes it easier for many object implementations in case we need to add more
    def __init__(self,name,img_path,x,y):
        self.name = name
        # Load and scale image
        raw_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale_by(raw_image, 3)
        self.image.set_colorkey(cfg.WHITE)
        self.particle_color = self.image.get_at((self.image.get_width() // 2,self.image.get_height() // 2))
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
                    if my_pet.inventory[self.name] > 0:
                        my_pet.feed(self.name) # This triggers the feeding logic
                        my_pet.inventory[self.name] -= 1
                
                        # Crumb particle implementation
                        for _ in range(15):
                            particles.append(Particle(self.rect.centerx,self.rect.centery,self.particle_color))
                        self.rect.center = self.original_pos

    def update(self,mouse_pos):
        if self.dragging:
            self.rect.center = mouse_pos
        else:
            self.rect.center = self.original_pos

    def draw(self,screen):
        if my_pet.inventory[self.name] > 0:
            screen.blit(self.image, self.rect)

# This class will be used to handle the feeding pet particles (crumbs)
# that should happen when the user feeds the pet in the feeding menu
class Particle:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        # Random direction when feeding
        self.vx = random.uniform(-3,3)
        self.vy = random.uniform(-5,-1) # goes upward at first
        self.life = 255 # so it dissapears

    def update(self,dt):
        self.x += self.vx
        self.vy += 0.2 # acts as gravity
        self.y += self.vy
        self.life -= 5 # fade speed
    
    def draw(self,screen):
        if self.life > 0:
            # Display a little pixel (crumb)
            crumb_rect = pygame.Rect(self.x, self.y, 4, 4)
            pygame.draw.rect(screen,self.color,crumb_rect)

# --- DYNAMIC CLOUDS ON BACKGROUND ---
cloud_images = []
for name in ["cloud_1.png","cloud_2.png","cloud_3.png"]:
    img = pygame.image.load(cfg.ASSETS_DIR / name).convert()
    img.set_colorkey(cfg.BLACK)
    cloud_images.append(img)

# Scaling the clouds
cloud_images = [pygame.transform.scale_by(img, 2) for img in cloud_images]


# Main class for cloud objects
class cloud:
    def __init__(self):
        self.image = random.choice(cloud_images)

        self.x = random.randint(0, cfg.WIDTH)
        self.y = random.randint(0,25) # only go to top section

        self.speed = random.uniform(0.02, 0.08)

    def update(self, dt):
        self.x += self.speed * dt

        # reset when it is offscreen
        if self.x > cfg.WIDTH + 100:
            self.x = -100
            self.y = random.randint(0,100)
            self.image = random.choice(cloud_images)
    def draw(self,screen):
        screen.blit(self.image, (self.x,self.y))

# Class for stars for when night is toggled
class Star:
    def __init__(self):
        self.x = random.randint(0,cfg.WIDTH)
        self.y = random.randint(0, int(cfg.HEIGHT * 0.5))
        self.speed = random.uniform(0.02, 0.06)
        self.size = random.randint(1,3)
    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = cfg.WIDTH
            self.y = random.randint(0, int(cfg.HEIGHT * 0.5))
    def draw(self, surface):
        pygame.draw.circle(surface, (255,255,255), (int(self.x),int(self.y)),self.size)

# -------------------------
# ---     VARIABLES     ---
# -------------------------

pygame.init()
pygame.mixer.init() # for sound effects and music 

# background music implementation
pygame.mixer.music.load(cfg.ASSETS_DIR / "forest.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) # Loop the background music indefinitely

victorySound = pygame.mixer.Sound(cfg.ASSETS_DIR / "victory_sound.ogg")
victorySound.set_volume(0.2) # Set the volume for the victory sound effect
eatingSound = pygame.mixer.Sound(cfg.ASSETS_DIR / "eatingSnd.wav")
eatingSound.set_volume(0.8) # Set the volume for the eating sound effect

# This code is for the custom font (pixelated font)
custom_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 32) # We will test out the font size
small_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 18)
medium_font = pygame.font.Font(cfg.FONTS_DIR / "Grand9k Pixel.ttf", 24)

# Window Title (Will be changed as we progress)
pygame.display.set_caption("A Foxy Pet Project")

# --- BACKGROUND IMAGES ---
background = pygame.image.load(cfg.ASSETS_DIR / "background.png").convert()
background = pygame.transform.scale(background, (cfg.WIDTH,cfg.HEIGHT))
background.set_colorkey(cfg.WHITE)
# Sky color: can be set to any value (for weather as well)
SKY_COLOR = (135,206,235)

# --- FEED, SLEEP, GAME BUTTONS ---
btn_width = 140
btn_height = 60
btn_y_pos = cfg.HEIGHT - 80
feed_button = pygame.Rect(20, btn_y_pos, btn_width, btn_height)
sleep_button = pygame.Rect(180, btn_y_pos,btn_width, btn_height)
game_button = pygame.Rect(340, btn_y_pos, btn_width, btn_height)

flappy_select_button = pygame.Rect(cfg.WIDTH // 2 - 120, 170, 240, 70)
snake_select_button = pygame.Rect(cfg.WIDTH // 2 - 120, 270, 240, 70)
future_game_button_2 = pygame.Rect(cfg.WIDTH // 2 - 120, 370, 240, 70)

change_weather_btn = pygame.Rect(cfg.WIDTH//2 - 140, 320, 280, 60)

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

# --- INFORMATION BUTTON ICON ---
raw_info_icon = pygame.image.load(cfg.ASSETS_DIR / "information_button_icon.png").convert()
raw_info_icon.set_colorkey(cfg.WHITE)
# Find the tightest box around the info icon
info_icon_area = raw_info_icon.get_bounding_rect()

cropped_info_icon = pygame.Surface(info_icon_area.size)
cropped_info_icon.fill(cfg.WHITE)
cropped_info_icon.set_colorkey(cfg.WHITE)
cropped_info_icon.blit(raw_info_icon, (0,0), info_icon_area)

info_icon = pygame.transform.scale_by(cropped_info_icon, 4)
info_icon_rect = info_icon.get_rect(topright=(cfg.WIDTH - 20, 20)) # will change to appropriate location

# --- STAT ICONS ---
energy_icon = pygame.transform.scale_by(pygame.image.load(cfg.ASSETS_DIR / "energy_icon.png").convert(), 2.25)
energy_icon.set_colorkey(cfg.WHITE)
hunger_icon = pygame.transform.scale_by(pygame.image.load(cfg.ASSETS_DIR / "hunger_food_icon.png").convert(), 3.5)
hunger_icon.set_colorkey(cfg.WHITE)

# -- DISPLAY ICONS --
def draw_stats(screen):
    # Colors for the icons
    NORMAL = cfg.BLACK
    LOW = (255,0,0) # Red when stats are low

    # Energy Icon
    e_x, e_y = 100, -5 # x and y for easier implementation
    screen.blit(energy_icon, (e_x,e_y))
    energy_color = LOW if my_pet.energy < 15 else NORMAL
    energy_txt = medium_font.render(f"{int(my_pet.energy)}%",True,energy_color)
    screen.blit(energy_txt, (e_x + 80, e_y + 35))

    # Hunger Icon
    h_x, h_y = 200, -30
    screen.blit(hunger_icon, (h_x, h_y))
    hunger_color = LOW if my_pet.hunger < 15 else NORMAL
    hunger_txt = medium_font.render(f"{int(my_pet.hunger)}%", True, hunger_color)
    screen.blit(hunger_txt, (h_x + 105, h_y + 59))

def draw_location(screen):
    if current_location and current_weather:
        category = current_weather.get("category", "").capitalize()
        txt = small_font.render(f"{current_location}: {category}", True, cfg.BLACK)
        screen.blit(txt, (20, 60))

def apply_weather_tint(screen, category):
    tint = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
    tint.set_alpha(80)

    if category == "cold":
        tint.fill((50, 80, 200))
    elif category == "hot":
        tint.fill((255, 120, 60))
    elif category == "temperate":
        return
    
    screen.blit(tint, (0, 0))
# --------------------------
# --- RUNNING PARAMETERS --- 
# --------------------------

Running = True
clock = pygame.time.Clock()
AUTOSAVE_INTERVAL = 10_000   # milliseconds (10 seconds)
autosave_timer = 0
scene = "MAIN" # for switching scenes
my_pet = Pet() # Initialize pet

# weather
current_location = None
current_weather = None

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

particles = [] # crumb particles

# Initialize cloud objects
clouds = [cloud() for _ in range(3)] # number of clouds

# Initialize star objects
stars = [Star() for _ in range(40)] # Number of stars

# Login Implementation
username = run_login_screen(screen=screen, pet=my_pet, game_clock=clock)
if not username:
    pygame.quit()
    quit()

# After the initial log in screen, reset clock so it doesn't accumulate dt
clock.tick()

ensure_user_exists(username)
stats, inv = load_pet_data(username)
if stats:
    my_pet.hunger, my_pet.happiness, my_pet.energy = stats
if inv:
    my_pet.inventory["Blueberry"] = inv[0]
    my_pet.inventory["Raspberry"] = inv[1]
    my_pet.inventory["Cookie"] = inv[2]
    
# --- LOAD PET DATA FROM DATABASE ---
stats, inv = load_pet_data(username)
print("Loaded Stats: ", stats)
print(f"Pet Stats - Hunger: {my_pet.hunger}, Happiness: {my_pet.happiness}, Energy: {my_pet.energy}")
if stats:
    my_pet.hunger, my_pet.happiness, my_pet.energy = stats
    
print("Loaded Inventory: ", inv)
print(f"Pet Inventory - Blueberry: {my_pet.inventory['Blueberry']}, Raspberry: {my_pet.inventory['Raspberry']}, Cookie: {my_pet.inventory['Cookie']}")
if inv:
    my_pet.inventory["Blueberry"] = inv[0]
    my_pet.inventory["Raspberry"] = inv[1]
    my_pet.inventory["Cookie"] = inv[2]
    

# -------------------------------
# --- MAIN RUNNING GAME LOOP ----
while Running:
    dt = clock.tick(cfg.FPS)    #frame rate/delta time

    autosave_timer += dt
    if autosave_timer >= AUTOSAVE_INTERVAL:
        save_pet_data(username, my_pet)
        autosave_timer = 0
        print("Autosaved pet data.")

    mouse_pos = pygame.mouse.get_pos()

    # Mouth Hitbox (Feeding)
    pet_rect = pygame.Rect(cfg.WIDTH // 2 - 40, cfg.HEIGHT // 2 - 40, 80, 80)
    
    # Cloud Implementation
    for cloud in clouds:
        cloud.update(dt)

    # Stars Implementation
    for star in stars:
        star.update()

    # Event Handler
    for event in pygame.event.get():
        # Quit button
        if event.type == pygame.QUIT:
            save_pet_data(username, my_pet)
            Running = False

        # Scene switch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if scene == "MAIN":
                if settings_btn.collidepoint(mouse_pos):
                    settings_open = not settings_open

                elif settings_open and change_weather_btn.collidepoint(mouse_pos):
                    location = pygame_text_input("Enter City Name: ")
                    if location:
                        current_location = location
                        current_weather = get_weather(location)

                if not settings_open and feed_button.collidepoint(mouse_pos):
                    scene = "FEED"

                    # if you click feed while sleeping, then awake the pet
                    my_pet.change_state("Idle")
                    
                    for food in foods:
                        food.dragging = False
                        food.rect.center = food.original_pos
                

                elif sleep_button.collidepoint(mouse_pos):
                    my_pet.sleep()
                    
                elif not settings_open and game_button.collidepoint(mouse_pos):
                    scene = "GAME_MENU"
                
            elif scene == "FEED":
                if back_btn_rect.collidepoint(mouse_pos): 
                    scene = "MAIN"
            
            elif scene == "GAME_MENU":
                if back_btn_rect.collidepoint(mouse_pos):
                    scene = "MAIN"

                elif flappy_select_button.collidepoint(mouse_pos):
                    result, blueberries_earned = run_flappy_game(screen=screen)
                    victorySound.play()
                    my_pet.inventory["Blueberry"] += blueberries_earned
                    clock.tick()    

                elif snake_select_button.collidepoint(mouse_pos):
                    rewards = snake.run_snake_game(screen)
                    
                    if rewards:       
                        victorySound.play()
                        my_pet.inventory["Blueberry"] += rewards["Blueberry"]
                        my_pet.inventory["Raspberry"] += rewards["Raspberry"]
                        my_pet.inventory["Cookie"] += rewards["Cookie"]

                        print("Rewards: ", rewards)
                    clock.tick()

                elif future_game_button_2.collidepoint(mouse_pos):
                    print("future game 2 goes here")
        
        
        # Dragging the food event
        if scene == "FEED":
            dragging_any_food = False # For feeding animation
            for food in foods:
                food.handle_events(event, mouse_pos, pet_rect)
                if food.dragging:
                    dragging_any_food = True
            
            # Triggering the feed animation when dragging
            if dragging_any_food:
                my_pet.change_state("Eating")
            elif my_pet.state == "Eating":
                my_pet.change_state("Idle")
    
    # ------------------
    #   DRAWING LOGIC
    # ------------------
    # Background set up

    screen.fill(SKY_COLOR)

    if my_pet.state == "Sleeping":
        screen.blit(night_overlay, (0,0))

    # Night stars implementation
    if my_pet.state == "Sleeping":
        for star in stars:
            star.draw(screen)

    # cloud implementation
    for cloud in clouds:
        cloud.draw(screen)
        
    screen.blit(background,(0,0))

    if current_weather:
        apply_weather_tint(screen, current_weather.get("category"))



    if scene == "MAIN":
        # Pet Display logic for main
        my_pet.update(dt)


        # If the pet is sleeping, darken the room
        if my_pet.state == "Sleeping":
            overlay = pygame.Surface((cfg.WIDTH,cfg.HEIGHT))
            overlay.set_alpha(160)
            overlay.fill((20,20,60))
            screen.blit(overlay,(0, 0))

        my_pet.draw(screen)
        # added stat info display
        draw_stats(screen)
        draw_location(screen)

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

            pygame.draw.rect(
                screen,
                BUTTON_HOVER if
                change_weather_btn.collidepoint(mouse_pos) else BUTTON_COLOR,
                    change_weather_btn
            )
            pygame.draw.rect(screen, cfg.BLACK, change_weather_btn, 3)

            txt = small_font.render("CHANGE LOCATION", True, cfg.WHITE)
            screen.blit(
                txt,
                (change_weather_btn.centerx - txt.get_width() // 2,
                 change_weather_btn.centery - txt.get_height() // 2)
            )

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
        draw_stats(screen)

        # Information icon functionality
        screen.blit(info_icon,info_icon_rect)

        if info_icon_rect.collidepoint(mouse_pos):
            feed_instrs = small_font.render("Drag food to the pet to feed!",True, cfg.BLACK)
            # text position
            screen.blit(feed_instrs, (info_icon_rect.left - 330, info_icon_rect.y + 50))

        my_pet.draw(screen)

        # This snippet of code is in charge of particles and fade out
        for p in particles[:]:
            p.update(dt)
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        # This snippet of code in in charge of the slots from the feeding menu
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
            if my_pet.inventory[food.name] > 0:
                food.update(mouse_pos)
                food.draw(screen)

                # This snippet is for drawing the quantity text near the slot
                qty_text = small_font.render(f"x{my_pet.inventory[food.name]}", True, cfg.BLACK)
                screen.blit(qty_text, (food.original_pos[0] - 20, food.original_pos[1] + 40))
                
    elif scene == "GAME_MENU":
        my_pet.update(dt)
        my_pet.draw(screen)
        screen.blit(back_icon, back_btn_rect)
        if back_btn_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER, back_btn_rect, border_radius=8)
        screen.blit(back_icon, back_btn_rect)

        title_txt = custom_font.render("SELECT GAME", True, cfg.BLACK)
        screen.blit(title_txt, (cfg.WIDTH // 2 - title_txt.get_width() // 2, 100))

        for rect, label in [
            (flappy_select_button, "FLAPPY"),
            (snake_select_button, "SNAKE"),
            (future_game_button_2, "COMING SOON")
        ]:
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, cfg.BLACK, rect, 4)
            txt = small_font.render(label, True, cfg.WHITE)
            screen.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2,
                               rect.y + (rect.height - txt.get_height()) // 2))
    
    # WHITE = (255,255,255)
    #screen.fill(cfg.WHITE) # white screen for now
    #Update the display tp show changes

    #for character display (template)
    #my_pet.draw(screen)
    pygame.display.flip()


# closing pygame and closing the program
pygame.quit()

sys.exit()