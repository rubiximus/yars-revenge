

import pygame

from asprite import ASprite
from vector import round_to_45, get_direction

class HomingBullet(ASprite):
    """A sprite that takes and follows a target
    """
    
    def __init__(self, sprite_filename, target, speed):
        """sprite_filename is the sprite file
        target is the Sprite that the bullet follows
        """
        
        ASprite.__init__(self, sprite_filename, speed)
        
        self.target = target
        self.speed = speed
        
        
    def update(self):
        """moves the bullet in the direction of the target"""
        
        selfx, selfy = self.rect.center
        targx, targy = self.target.rect.center
        direction = round_to_45(get_direction(self.rect.center, self.target.rect.center))
        
        self.move(direction)
