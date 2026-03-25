import pygame

# This is a module that will help us render the images
# and help us overall with the animation making it modular
# that way we can call different types of sprite sheets such as
# a mood sprite sheet or a hungry animation sprite sheet.

class Animator:
    #Initializer
    def __init__(self,sprite_sheet_path, frame_width, frame_height, scale=1):
        self.sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.frames = self.load_frames = 0
        self.time = 0
    def load_frames(self):
        # this section will make it so we can cut the sprite sheet into individual frames
        frames = []
        sheet_width = self.sheet.get_width()
        for x in range(0, sheet_width, self.frame_width):
            frame = self.sheet.subsurface((x,0,self.frame_width, self.frame_height))
            if self.scale != 1:
                frame = pygame.transform.scale(frame,(self.frame_width * self.scale, self.frame_height * self.scale))
            frame.append(frame)
        return frames
    
    def update(self,dt,speed=0.1):
        # This will determine how fast the frames will switch
        self.timer += dt
        if self.timer >= speed:
            self.time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self,screen,x,y):
        # This function will render the image as per accounted sprite sheet
        screen.blit(self.frames[self.current_frame], (x,y))
