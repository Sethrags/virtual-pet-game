# Filename: animation_module.py
# Author: Jorge
# Description: This file implements the Animator class, which is responsible for handling sprite sheet animations in the Tamagotchi game. 
# This is a module will help us render the images and help overall with the animation making it modular that way we can call different
#  types of sprite sheets such as a mood sprite sheet or a hungry animation sprite sheet.
import pygame

# Animator class
# This class is responsible for handling sprite sheet animations. It loads a sprite sheet, cuts it into individual frames, 
# and manages the timing of frame updates to create smooth animations. The class provides methods to update the animation 
# based on a timer and to draw the current frame on the screen at specified coordinates.
class Animator:

    #Initializer
    # The initializer takes the path to the sprite sheet, the width and height of each frame, and an optional scale factor. 
    # It loads the sprite sheet, sets the color key for transparency, and calls the load_frames method to cut the sprite sheet into individual frames. 
    # It also initializes variables for timing and frame management.
    def __init__(self,sprite_sheet_path, frame_width, frame_height, scale=1):
        self.sheet = pygame.image.load(sprite_sheet_path).convert()
        self.sheet.set_colorkey((255,255,255))
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.frames = self.load_frames()
        self.time = 0
        self.timer = 0
        self.current_frame = 0

    # load_frames
    # This method cuts the sprite sheet into individual frames based on the specified frame width and height.
    # It calculates the number of frames in the sprite sheet and extracts each frame using the subsurface method.
    # If a scale factor is provided, it scales each frame accordingly. The method returns a list of frames that can be used for animation.
    # The frames are stored in the self.frames list, which is used by the update and draw methods to manage the animation.
    def load_frames(self):
        frames = [] # List to store the individual frames extracted from the sprite sheet
        sheet_width = self.sheet.get_width() # Get the width of the sprite sheet to calculate how many frames it contains

        num_frames = sheet_width // self.frame_width # Calculate the number of frames in the sprite sheet 

        # Loop through each frame in the sprite sheet and extract it using the subsurface method
        for i in range(num_frames):
            x = i * self.frame_width # Calculate the x-coordinate for the current frame based on its index and the frame width
            frame = self.sheet.subsurface((x,0,self.frame_width,self.frame_height))
                
            # If a scale factor is provided, scale the frame accordingly using the pygame.transform.scale method
            if self.scale != 1:
                new_size = (int(self.frame_width * self.scale), int(self.frame_height * self.scale))
                frame = pygame.transform.scale(frame,new_size)
            frames.append(frame)
        return frames

    # update
    # This method updates the animation based on a timer. It takes the delta time (dt) since 
    # the last update and an optional speed parameter that controls how fast the frames switch
    def update(self,dt,speed=200):
        # This will determine how fast the frames will switch
        self.timer += dt
        if self.timer >= speed:
            self.timer -= speed
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    # draw
    # This method draws the current frame of the animation on the screen at specified x and y coordinates. 
    # It uses the blit method to render the current frame from the self.frames list onto the provided screen.
    def draw(self,screen,x,y):
        screen.blit(self.frames[self.current_frame], (x,y))
