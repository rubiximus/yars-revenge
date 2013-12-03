"""

enemy_base.py

The enemy base is the main enemy of the game. Its behavior is split into three
different states:

1. moving along the right side of the screen at a steady pace
2. preparing to launch (beginning to swirl)
3. flying in a straight line as a swirl

This behavior is implemented as a state machine. EnemyBase is the state manager,
MoverBase performs state 1, SpinnerBase is state 2, and ShooterBase is state 3.
These classes contain both the behavior of their states as well as the rules for
transitioning to the next state. For more information, see the doc string for
each class.

State transitions operate as a conversation between the manager and the states:
High level transition calls are allowed by calling transition_<state>() in the
manager class. This calls a become_<state>() in the current state, which may have
no behavior (e.g. if such a transition is not allowed) or may call a
start_<state>() in the manager which finally changes the state.

Alternatively the start_<state>() function may be called directly to force a
jump between states, but this is not recommended.

"""

import pygame
from pygame import key
from pygame.locals import *

from asprite import ASprite
from animated_facing_sprite import AnimatedFacingSprite
from vector import *
import options

class EnemyBase(ASprite):
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
        
        self.mover_args = mover_args
        self.spinner_args = spinner_args
        self.shooter_args = shooter_args
        
        self.target = target
        
        self.mover_state = MoverBase(self, *self.mover_args)
        self.current_state = self.mover_state
        
        
    def update(self):
        self.current_state.update()
        self.image = self.current_state.image
        self.rect = self.current_state.rect
        self.mask = self.current_state.mask
        
        
    def transition_mover(self):
        self.current_state.become_mover()
        
    def transition_spinner(self):
        self.current_state.become_spinner()
        
    def transition_shooter(self):
        self.current_state.become_shooter()
        
        
    def start_mover(self):
        mover = MoverBase(self, *self.mover_args)
        self.mover_state = mover
        self.change_state(mover)
        
    def start_spinner(self, position):
        spinner = SpinnerBase(self, position, self.target, *self.spinner_args)
        self.change_state(spinner)
        
    def start_shooter(self, position, direction):
        shooter = ShooterBase(self, position, direction, *self.shooter_args)
        self.change_state(shooter)
        
    def resume_mover_state(self):
        self.change_state(self.mover_state)
        
        
    def change_state(self, new_state):
        self.current_state = new_state
        
    def get_state(self):
        return self.current_state    
    
    def get_state_number(self):
        """Returns a number corresponding to the current state.
        
        See the docstrings for this file and for each state class to see the numbers.
        """
        
        return self.current_state.STATE_NUMBER
        
        
    def is_followable(self):
        """Returns whether the current state is followable (by the EnemyShield)
        
        Docstrings for state classes should specify whether the state is followable
        """
        
        return self.current_state.IS_FOLLOWABLE
        
        
    def get_rect(self):
        """Used for EnemyShield (and collisions?)"""
        
        return self.current_state.rect

        
class MoverBase(ASprite):
    """State 1: Moves up and down along right side of screen.
    
    MoverBase should be followable by the shield.
    """
    
    def __init__(self, manager, sprite_filename, top, bottom, speed):
        """manager is the root EnemyBase object
        top, bottom are the boundaries of movement (rect.top <= top, etc)
        """
        
        super(MoverBase, self).__init__(sprite_filename, speed)
        
        self.rect.topright = (options.width, top)
        
        self.top = top
        self.bottom = bottom
        self.current_dir = SOUTH
        self.speed = speed
        self.manager = manager
        
        self.STATE_NUMBER = manager.MOVING
        self.IS_FOLLOWABLE = True
        
        
    def update(self):
        self.move(self.current_dir)
        
        if self.rect.bottom >= self.bottom:
            self.current_dir = NORTH
        elif self.rect.top <= self.top:
            self.current_dir = SOUTH
            
        #rule for changing state -- should be probabilistic/time-based later
        key_states = key.get_pressed()
        if key_states[K_1]: self.become_spinner()
            
            
    def become_mover(self):
        return False
    
    def become_spinner(self):
        self.manager.start_spinner(self.rect.center)
        return True
        
    def become_shooter(self):
        return False
            
            
class SpinnerBase(AnimatedFacingSprite):
    """State 2: Spins in place for a period of time. In the original game the
    base should continue to move as in MoverBase, but currently it becomes
    stationary for simplicity reasons.
    
    SpinnerBase should be followable by the shield.
    
    Note: though this is an AnimatedFacingSprite the spritesheet should only have one row
    (and therefore self.current_dir should never be changed from NORTH)"""
    
    def __init__(self, manager, position, target, sprite_sheet, height, width, delay,
                targ_time, shoot_time):
        """manager is the root EnemyBase object
        position is the sprite's rect.center coordinates (taken from the moving state)
        sprite_sheet, etc are AnimatedFacingSprite args
        
        targ_time is the frame (from start) when target direction is taken
        shoot_time is the frame (from start) when spinner becomes shooter and begins movement
        """
        
        super(SpinnerBase, self).__init__(sprite_sheet, height, width, delay, 0)
        self.rect.center = position
        self.manager = manager
        self.target = target
        
        self.targ_time = targ_time
        self.shoot_time = shoot_time
        self.tick = 0
        
        self.STATE_NUMBER = manager.SPINNING
        self.IS_FOLLOWABLE = True
        
        
    def update(self):
        super(SpinnerBase, self).update()
        
        self.tick += 1
        
        if self.tick == self.targ_time:
            self.target_direction = normalize(get_direction(self.rect.center, self.target.rect.center))
        if self.tick == self.shoot_time:
            self.become_shooter()
        
        
    def become_mover(self):
        return False
        
    def become_spinner(self):
        return False
    
    def become_shooter(self):
        self.manager.start_shooter(self.rect.center, self.target_direction)
        return True
        
        
class ShooterBase(AnimatedFacingSprite):
    """State 3: Moves ("shoots") in the given direction until offscreen.
    
    ShooterBase should not be followable by the shield.
    
    Note: though this is an AnimatedFacingSprite the spritesheet should only have one row
    (and therefore self.current_dir should never be changed from NORTH)
    """
    
    def __init__(self, manager, position, direction, sprite_sheet, height, width, delay, speed):
        """manager is the base EnemyBase object
        position is the rect.center coordinates (taken from the spinning state)
        direction is a vector
        """
        
        super(ShooterBase, self).__init__(sprite_sheet, height, width, delay, speed)
        
        self.manager = manager
        self.rect.center = position
        self.direction = direction
        
        self.STATE_NUMBER = manager.SHOOTING
        self.IS_FOLLOWABLE = False
        
        
    def update(self):
        super(ShooterBase, self).update()
        
        super(AnimatedFacingSprite, self).move(self.direction)
        
        if self.rect.left <= 0 or self.rect.top <= 0 or self.rect.bottom >= options.height:
            self.become_mover()
        
        
    def become_mover(self):
        self.manager.resume_mover_state()
        
    def become_spinner(self):
        self.manager.start_spinner(self.rect.center)
        
    def become_shooter(self):
        return False
