"""

infoscreen.py

Contains the InfoScreen class, which is a state for the info screen
which shows lives and score before and after levels

"""

import pygame
from pygame.locals import *
from pygame.font import Font, get_default_font

from gamestate import GameState
import event_handlers

import options

class InfoScreen(GameState):
    """InfoScreen is a GameState which shows lives and score and waits for input
    for input to start the next state
    """

    def __init__(self, manager, score, lives, next_state):
        GameState.__init__(self, manager)

        sys_font = Font(get_default_font(), options.font_size)
        self.score_text = sys_font.render(str(score), True, options.white)
        self.lives_text = sys_font.render(str(lives), True, options.white)

        self.next_state = next_state


    def handle_events(self, events, keys):
        return (event_handlers.check_quit(events, keys) and
                event_handlers.check_shoot_button(events, keys, self.change_state))


    def draw(self, screen):
        right_edge = options.width * 2 / 3
        score_height = options.height / 3
        lives_height = score_height + options.height / 6
        screen.blit(self.score_text,
                    self.score_text.get_rect(midright = (right_edge, score_height)))
        screen.blit(self.lives_text,
                    self.lives_text.get_rect(midright = (right_edge, lives_height)))


    def change_state(self):
        self.manager.change_state(self.next_state)