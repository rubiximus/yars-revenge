"""

title.py

Contains the Title class, which is a state for the title screen

"""

import pygame
from pygame.locals import *
from pygame.font import Font, get_default_font

from gamestate import GameState
import event_handlers

import options

class Title(GameState):
    """Title is a GameState which shows a title screen and waits for input
    to start a level
    """

    def __init__(self, manager):
        GameState.__init__(self, manager)

        sys_font = Font(get_default_font(), options.font_size)
        self.message1 = sys_font.render("Andrew's Bitchin' Yars' Revenge Clone",
                                        True, options.white)
        self.message2 = sys_font.render("Press shoot button (space) to start.",
                                        True, options.white)


    def handle_events(self, events, keys):
        return (event_handlers.check_quit(events, keys) and
                event_handlers.check_shoot_button(events, keys, self.manager.new_game))


    def draw(self, screen):
        sys_font = Font(get_default_font(), options.font_size)


        screen.blit(self.message1, self.message1.get_rect(center = (400, 100)))
        screen.blit(self.message2, self.message2.get_rect(center = (400, 150)))
