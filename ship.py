

#import pygame

from asprite import ASprite
from animated_facing_sprite import AnimatedFacingSprite
import options

class Ship(AnimatedFacingSprite):
    """The player's sprite ship
    
    Moves in eight directions with screen wraparound -- see move() docstring
    """

    def __init__(self, sprite_sheet, height, width, delay, speed):
        """delay is the time (in frames) spent on each image
        sprite_sheet is the filename of the sprites
        height, width are the dimensions of the sprite
        """
        
        super(Ship, self).__init__(sprite_sheet, height, width, delay, speed)
        
        
    def move(self, direction):
        """can't move off left or right edges and loops around top and bottom
        otherwise moves same as AnimatedFacingSprite
        """
        
        super(Ship, self).move(direction)
        
        #if ship is off left or right edges, "nudge" back to the edge
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > options.width:
            self.rect.right = options.width
            
        #if ship is off top or bottom edges, teleport to opposite edge
        if self.rect.top < 0:
            self.rect.bottom = options.height
        if self.rect.bottom > options.height:
            self.rect.top = 0

            
class Bullet(ASprite):
    """The player's bullet
    
    Moves in a single direction until offscreen
    """
    
    def __init__(self, sprite_filename, speed, position, direction):
        super(Bullet, self).__init__(sprite_filename, speed)
        self.rect.center = position
        self.direction = direction
        
        
    def update(self):
        super(Bullet, self).move(self.direction)
        
        if (self.rect.left < 0 or self.rect.top < 0 or
            self.rect.right > options.width or self.rect.bottom > options.height):
            self.kill()
