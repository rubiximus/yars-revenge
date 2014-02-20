"""

enemy_base.py

The enemy base is the main enemy of the game. Its behavior is split into three
different states:

1. moving along the right side of the screen at a steady pace
2. preparing to launch (beginning to swirl)
3. flying in a straight line as a swirl

This behavior is implemented as a state machine. EnemyBase is the state manager,
MovingBase performs state 1, SpinningBase is state 2, and ShootingBase is state 3.

"""

from random import random

import pygame
from pygame.locals import *

from statemachine import Manager, State
from asprite import ASprite
from animated_facing_sprite import AnimatedFacingSprite
from vector import *
import options

class EnemyBase(Manager):
    """State manager class for the enemy base
    
    Contains class constants MOVING, SPINNING, and SHOOTING which are the
    state numbers for the corresponding states."""
    
    MOVING = 1
    SPINNING = 2
    SHOOTING = 3
    
    def __init__(self, mover_args, spinner_args, shooter_args, target):
        """mover_args, spinner_args, and shooter_args are tuples of arguments
        target is the player's sprite (the sprite to fire toward)
        """

        Manager.__init__(self)
        
        self.mover_args = mover_args
        self.spinner_args = spinner_args
        self.shooter_args = shooter_args
        
        self.target = target
        
        self.mover_state = MovingBase(self, *self.mover_args)
        self.change_state(self.mover_state)


    def start_mover(self):
        mover = MovingBase(self, *self.mover_args)
        self.mover_state = mover
        self.change_state(mover)


    def start_spinner(self, position):
        spinner = SpinningBase(self, position, self.target, *self.spinner_args)
        self.change_state(spinner)


    def start_shooter(self, position, direction):
        shooter = ShootingBase(self, position, direction, *self.shooter_args)
        self.change_state(shooter)


    def resume_mover_state(self):
        self.change_state(self.mover_state)
        
        
    def is_followable(self):
        """Returns whether the current state is followable (by the EnemyShield)
        
        Docstrings for state classes should specify whether the state is followable
        """
        
        return self.current_state.IS_FOLLOWABLE
        
        

class MovingBase(State):
    """State 1: Moves up and down along right side of screen.
    
    MovingBase should be followable by the shield.
    """
    
    def __init__(self, manager, sprite_filename, speed, top, bottom, avg_transition):
        """manager is the root EnemyBase object
        top, bottom are the boundaries of movement (rect.top <= top, etc)
        """
        
        State.__init__(self, manager)
        
        self.sprite = ASprite(sprite_filename, speed)

        self.sprite.rect.topright = (options.width, top)
        
        self.top = top
        self.bottom = bottom
        self.current_dir = SOUTH

        self.transition_probability = 1 / (avg_transition * options.max_framerate)
        
        self.STATE_NUMBER = manager.MOVING
        self.IS_FOLLOWABLE = True
        
        
    def update(self):
        self.sprite.move(self.current_dir)

        if random() <= self.transition_probability:
            self.transition_to(self.manager.SPINNING)
        
        if self.sprite.rect.bottom >= self.bottom:
            self.current_dir = NORTH
        elif self.sprite.rect.top <= self.top:
            self.current_dir = SOUTH


    def transition_to(self, new_state_number):
        if new_state_number == self.manager.SPINNING:
            self.manager.start_spinner(self.sprite.rect.center)
            return True

        return False
            
            

class SpinningBase(State):
    """State 2: Spins in place for a period of time. In the original game the
    base should continue to move as in MovingBase, but currently it becomes
    stationary for simplicity reasons.
    
    SpinningBase should not be followable by the shield.
    
    Note:SpinningBase.sprite is an AnimatedFacingSprite that only faces NORTH
    """
    
    def __init__(self, manager, position, target, sprite_sheet, height, width, delay,
                targ_time, shoot_time):
        """manager is the root EnemyBase object
        position is the sprite's rect.center coordinates (taken from the moving state)
        sprite_sheet, etc are AnimatedFacingSprite args
        
        targ_time is the frame (from start) when target direction is taken
        shoot_time is the frame (from start) when spinner becomes shooter and begins movement
        """
        
        State.__init__(self, manager)

        self.sprite = AnimatedFacingSprite(sprite_sheet, height, width, delay, 0)
        self.sprite.rect.center = position

        self.target = target
        
        self.targ_time = targ_time
        self.shoot_time = shoot_time
        self.tick = 0
        
        self.STATE_NUMBER = manager.SPINNING
        self.IS_FOLLOWABLE = False
        
        
    def update(self):
        self.sprite.update()
        
        self.tick += 1
        
        if self.tick == self.targ_time:
            self.target_direction = normalize(get_direction(self.sprite.rect.center, self.target.rect.center))
        if self.tick == self.shoot_time:
            self.transition_to(self.manager.SHOOTING)


    def transition_to(self, new_state_number):
        if new_state_number == self.manager.SHOOTING:
            self.manager.start_shooter(self.sprite.rect.center, self.target_direction)

        return False
        
        

class ShootingBase(State):
    """State 3: Moves ("shoots") in the given direction until offscreen.
    
    ShootingBase should not be followable by the shield.
    
    Note:ShootingBase.sprite is an AnimatedFacingSprite that only faces NORTH
    """
    
    def __init__(self, manager, position, direction, sprite_sheet, height, width, delay, speed):
        """manager is the base EnemyBase object
        position is the rect.center coordinates (taken from the spinning state)
        direction is a vector
        """
        
        State.__init__(self, manager)

        self.sprite = AnimatedFacingSprite(sprite_sheet, height, width, delay, speed)
        self.sprite.rect.center = position

        self.direction = direction
        
        self.STATE_NUMBER = manager.SHOOTING
        self.IS_FOLLOWABLE = False
        
        
    def update(self):
        self.sprite.update()
        ASprite.move(self.sprite, self.direction)

        rect = self.sprite.rect
        
        if rect.left <= 0 or rect.top <= 0 or rect.bottom >= options.height:
            self.transition_to(self.manager.MOVING)


    def transition_to(self, new_state_number):
        if new_state_number == self.manager.MOVING:
            self.manager.resume_mover_state()
            return True

        if new_state_number == self.manager.SPINNING:
            self.manager.start_spinner(self.sprite.rect.center)

        return False
