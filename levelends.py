"""

levelends.py

"""

import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, collide_mask, spritecollide, groupcollide

from gamestate import GameState

import event_handlers

from options import *
from vector import *
from ship import Ship, Bullet
from enemy_base import EnemyBase
from formations import formation, formation_center
from enemy_shield import EnemyShield
from homing_bullet import HomingBullet
from cannon import Cannon

class DeathAnimation(GameState):
    """Plays an animation where the player spins around in a circle
    Other sprites are drawn but stay motionless
    next_level is the level to be resumed after this animation
    """

    def __init__(self, manager, player, other_sprites, next_level):
        self.manager = manager
        self.player = player
        self.other_sprites = other_sprites
        self.next_level = next_level

        self.tick = 0
        self.delay = 4
        self.total_runtime = 64


    def update(self):
        self.tick += 1

        if self.tick == self.total_runtime:
            self.manager.kill_player(self.next_level)

        elif self.tick % self.delay == 0:
            self.player.turn_right()

        self.player.update_direction()


    def handle_events(self, events, keys):
        return event_handlers.check_quit(events, keys)


    def draw(self, screen):
        self.player.draw(screen)

        for curr in self.other_sprites:
            curr.draw(screen)


class WinAnimation(GameState):
    """All sprites but the player disappear. The player has free movement for a few seconds.
    """

    def __init__(self, manager, player):
        self.manager = manager
        self.player = player

        self.tick = 0
        self.total_runtime = 120


    def update(self):
        self.tick += 1

        if self.tick == self.total_runtime:
            self.manager.next_level()
            
        self.player.update()

    
    def handle_events(self, events, keys):
        return (event_handlers.check_quit(events, keys) and
                event_handlers.move_player(events, keys, self.player))


    def draw(self, screen):
        self.player.draw(screen)
