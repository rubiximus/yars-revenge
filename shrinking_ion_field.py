"""

shrinking_ion_field.py

This is used for the explosion effect in the win animation

"""

import pygame
from pygame import draw
from pygame import Surface
from pygame import PixelArray
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.mask import Mask

from ion_field import IonField

class ShrinkingIonField(IonField):
    """IonField which will smoothly shrink from the top and bottom every frame"""

    def __init__(self, left, top, width, height, noise_width, noise_height, delay, shrink_rate):
        IonField.__init__(self, left, top, width, height, noise_width, noise_height, delay)

        self.shrink_rate = shrink_rate
        self.crop_top = int(shrink_rate / 2)

    def update(self):
        self.shrink()
        IonField.update(self)


    def shrink(self):
        self.height = max(self.height - self.shrink_rate, 0)

        #copy the existing noise, cropping off the top and bottom
        temp_image = Surface((self.width, self.height))
        temp_image.blit(self.image, Rect(0, 0, 0, 0), Rect(0, self.crop_top, self.width, self.height))
        self.image = temp_image
        
        self.mask = Mask((self.width, self.height))
        self.mask.fill()

        self.top = self.top + self.crop_top

        self.rect = Rect(self.left, self.top, self.width, self.height)
