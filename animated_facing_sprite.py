

import pygame

from asprite import ASprite
from vector import *
from utilities import *

#dictionary from vector constants to list indeces
DIRECTIONS = {NORTH:0, NORTHEAST:1, EAST:2, SOUTHEAST:3, SOUTH:4, SOUTHWEST:5, WEST:6, NORTHWEST:7}

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
        
        #doesn't seem to be needed right now
        #super(ASprite, self).__init__()
        
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
        
        direction should be a tuple (vector.py constant)
        """
        
        if direction in DIRECTIONS.keys():
            self.current_dir = direction
        else:
            #TODO: use vector.round_to_45(); requires it to return integer tuples
            print("That isn't a good direction you dummy!")
            return
        
        super(AnimatedFacingSprite, self).move(direction)
        
        
    def update(self):
        """updates animation's "tick" and frame"""
        
        self.current_step = self.current_step + 1
        if self.current_step >= self.delay:
            self.current_step = 0
            self.current_frame = (self.current_frame + 1) % len(self.images[0])
            
        direction_index = DIRECTIONS[self.current_dir]
        frame_index = self.current_frame
        self.image = self.images[direction_index][frame_index]
        self.mask = self.masks[direction_index][frame_index]
        
        
    def get_direction(self):
        return self.current_dir
        
        

