"""

ion_field.py

This is the neutral zone in the middle of the screen.

"""

from random import randint, choice

import pygame
from pygame import draw
from pygame import Surface
from pygame import PixelArray
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.mask import Mask

from statemachine import Manager, State
from asprite import ASprite

COLORS = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), 
          (255, 0, 0), (0, 255, 0), (0, 0, 255),
          (200, 150, 0), (200, 200, 0), (150, 0, 200), (0, 150, 200)]

class IonField(Sprite):
    """Sprite that draws a bunch of random horizontal lines inside a rectangle."""
    
    def __init__(self, left, top, width, height, noise_width, noise_height, delay):
        Sprite.__init__(self)

        self.top = top
        self.left = left
        self.width = width
        self.height = height

        self.image = Surface((self.width, self.height))
        self.rect = Rect(left, top, self.width, self.height)
        self.rect = Rect(left, top, 0, 0)
        self.mask = Mask((self.width, self.height))
        self.mask.fill()

        self.noise_width = noise_width
        self.noise_height = noise_height

        self.tick = 0
        self.delay = delay


    def update(self):
        self.tick = self.tick + 1
        if self.tick % self.delay == 0:
            self.generate_noise()


    def draw(self, screen):
        screen.blit(self.image, self.rect)
    

    def generate_noise(self):
        for col in range(0, self.image.get_width(), self.noise_width):
            for row in range(0, self.image.get_height(), self.noise_height):
                c = choice(COLORS)
                draw.rect(self.image, c, Rect(col, row, self.noise_width, self.noise_height))
