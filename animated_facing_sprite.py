

import pygame
from pygame import Surface, mask
from pygame.sprite import Sprite

from asprite import ASprite
from vector import *

#dictionary from vector constants to list indeces
DIRECTIONS = {NORTH:0, NORTHEAST:1, EAST:2, SOUTHEAST:3, SOUTH:4, SOUTHWEST:5, WEST:6, NORTHWEST:7}

#lookup tables for turning
TURN_RIGHT = {NORTH:NORTHEAST, NORTHEAST:EAST, EAST:SOUTHEAST, SOUTHEAST:SOUTH, SOUTH:SOUTHWEST, SOUTHWEST:WEST, WEST:NORTHWEST, NORTHWEST:NORTH}
TURN_LEFT = {NORTH:NORTHWEST, NORTHEAST:NORTH, EAST:NORTHEAST, SOUTHEAST:EAST, SOUTH:SOUTHEAST, SOUTHWEST:SOUTH, WEST:SOUTHWEST, NORTHWEST:WEST}

class AnimatedFacingSprite(ASprite):
    """Special sprite class that has an animated image for each direction
    Each row of the source sprite file should be the animation for one direction
    with top row as N and going clockwise; animations read left to right
    
    images is the 2D array, indexed [row][col], ie [dir][frame]
    """
    
    def __init__(self, sprite_sheet, height, width, delay, speed):
        """delay is the time (in frames) spent on each image
        sprite_sheet is the filename of the sprites
        """
        
        Sprite.__init__(self)
        
        self.delay = delay
        self.images, self.masks = split_frames(sprite_sheet, height, width)
        
        #by default, sprite appears in upper right, facing north at frame 0
        self.image = self.images[0][0]
        self.mask = self.masks[0][0]
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.current_dir = NORTH
        self.current_frame = 0
        self.current_step = 0
        
        self.speed = speed
        
        
    def move(self, direction):
        """moves the sprite in the given direction
        
        direction should be a tuple representing a unit vector
        """
        
        if direction in DIRECTIONS.keys():
            self.current_dir = direction
        else:
            self.current_dir = round_to_45(direction)
        
        ASprite.move(self, direction)
        
        
    def update(self):
        """updates animation and direction"""

        self.update_animation()
        self.update_direction()


    def update_animation(self):
        """updates animation's frame only"""

        self.current_step += 1
        if self.current_step >= self.delay:
            self.current_step = 0
            self.current_frame = (self.current_frame + 1) % len(self.images[0])


    def update_direction(self):
        """updates sprite's direction only"""

        direction_index = DIRECTIONS[self.current_dir]
        frame_index = self.current_frame
        self.image = self.images[direction_index][frame_index]
        self.mask = self.masks[direction_index][frame_index]


    def turn_right(self):
        """turns the sprite one eighth turn to the right"""

        self.current_dir = TURN_RIGHT[self.current_dir]


    def turn_left(self):
        """turns the sprite one eighth turn to the left"""

        self.current_dir = TURN_LEFT[self.current_dir]
        
        
    def get_direction(self):
        return self.current_dir

    def set_direction(self, new_dir):
        self.current_dir = new_dir
        
        
        
def split_frames(filename, height, width, single_row=False):
    """Splits a multi-sprite file into subsurfaces.
    filename is the image file containing the sprites
    height, width are the dimensions of the sprites
    
    returns a 2D list of Surfaces indexed [row][col]
    returns normal list when image file is one row and single_row is set to True
    """
    
    parent = pygame.image.load(filename).convert_alpha()
    parent_width, parent_height = parent.get_size()
    parent_rows = int(parent.get_height() / height)
    parent_cols = int(parent.get_width() / width)
    
    if parent_rows == 1 and single_row:
        return split_row(parent, parent_cols, 0, height, width)
    
    images = []
    masks = []
    
    for row in range(parent_rows):
        current_images, current_masks = split_row(parent, parent_cols, row, height, width)
        images.append(current_images)
        masks.append(current_masks)
        
    return images, masks
    
    
def split_row(parent, parent_cols, row, height, width):
    """split_frame helper function
    splits a single row of source surface
    """
    
    images = []
    masks = []
    
    for col in range(parent_cols):
        current_image = parent.subsurface((col*width, row*height, width, height))
        images.append(current_image)
        masks.append(mask.from_surface(current_image))
        
    return images, masks
