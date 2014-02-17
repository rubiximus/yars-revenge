"""

title.py

Contains the Title class, which is a state for the title screen

"""

import pygame
from pygame.locals import *
from pygame.font import Font, get_default_font

from gamestate import GameState

import options

class Title(GameState):
    """Title is a GameState which shows a title screen and waits
    for input to start a level
    """

    def __init__(self, manager):
        super(Title, self).__init__(manager)


    def handle_events(self, events, keys):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == K_ESCAPE:
                    return False
                else:
                    self.manager.new_game()

        return True


    def draw(self, screen):
        sys_font = Font(get_default_font(), options.font_size)

        message1 = sys_font.render("Andrew's Bitchin' Yars' Revenge Clone", True, options.white)
        message2 = sys_font.render("Press a key to start", True, options.white)

        screen.blit(message1, message1.get_rect(center = (400, 100)))
        screen.blit(message2, message2.get_rect(center = (400, 150)))
