

import pygame
from pygame import mask
from pygame.sprite import Sprite

from vector import *

class ASprite(Sprite):
    """Advanced sprite class that adds basic methods for moving and drawing
    """
    
    def __init__(self, sprite_filename, speed):
    
        Sprite.__init__(self)
        
        self.image = pygame.image.load(sprite_filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        
        self.speed = speed
        
        
    def move(self, direction):
        """direction should be a 2D vector"""
        
        self.rect.center = add(self.rect.center, scale(direction, self.speed))
        
        
    def draw(self, screen):
    
        screen.blit(self.image, self.rect)
        
        
    def get_rect(self):
        return self.rect
