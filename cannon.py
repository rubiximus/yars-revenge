"""

cannon.py

The cannon is the player's special weapon, notable for being the only way to
destroy the enemy base. Its behavior is split into three states:

1. Deactivated (no image or behavior)
2. Standby (visible on right side of screen; follows player's vertical position)
3. Firing across the screen

This behavior is implemented as a state machine. Cannon is the state manager,
DeactivatedCannon is state 1, StandbyCannon is state 2, and FiringCannon is state 3.

State transitions operate as a conversation between the manager and the states:
High level transition calls are allowed by calling transition_<state>() in the
manager class. This calls a become_<state>() in the current state, which may have
no behavior (e.g. if such a transition is not allowed) or may call a
start_<state>() in the manager which finally changes the state.

Alternatively the start_<state>() function may be called directly to force a
jump between states, but this is not recommended.

"""

from pygame import Surface, Rect
from pygame.sprite import Sprite

from asprite import ASprite
from vector import *
import options

class Cannon():
    """State manager for the cannon
    
    Contains class constants DEACTIVATED, STANDBY, and FIRING which are the
    state numbers for the corresponding states."""
    
    DEACTIVATED = 1
    STANDBY = 2
    FIRING = 3
    
    def __init__(self, deactivated_args, standby_args, firing_args, target):
        """*_args are tuples of arguments; see corresponding classes' __init__()
        target is the player's sprite (the sprite to follow on standby)
        """
        
        self.deactivated_args = deactivated_args
        self.standby_args = standby_args
        self.firing_args = firing_args
        
        self.target = target
        
        self.start_deactivated()
        
        
    def update(self):
        self.current_state.update()
        
        
    def draw(self, screen):
        self.current_state.draw(screen)
        
        
    def transition_deactivated(self):
        return self.current_state.become_deactivated()
        
    def transition_standby(self):
        return self.current_state.become_standby()
        
    def transition_firing(self):
        return self.current_state.become_firing()
        
        
    def start_deactivated(self):
        deactive = DeactivatedCannon(self, *self.deactivated_args)
        self.change_state(deactive)
        
    def start_standby(self):
        standby = StandbyCannon(self, self.target, *self.standby_args)
        self.change_state(standby)
        
    def start_firing(self, position):
        firing = FiringCannon(self, position, *self.firing_args)
        self.change_state(firing)
        
        
    def change_state(self, new_state):
        self.current_state = new_state
        
    def get_state(self):
        return self.current_state        
        
    def get_state_number(self):
        """Returns a number corresponding to the current state.
        
        See the docstrings for this file and for each state class to see the numbers.
        """
        
        return self.current_state.STATE_NUMBER
        
        
class DeactivatedCannon(Sprite):
    """State 1: no image or behavior. All functions do nothing. Pretty simple.
    
    For collision simplification this class is an empty sprite with
    image and rect of zero area.
    """
    
    def __init__(self, manager):
        self.manager = manager
        
        self.image = Surface((0, 0))
        self.rect = Rect(0, 0, 0, 0)
        
        self.STATE_NUMBER = manager.DEACTIVATED
        
        
    def update(self):
        return
        
        
    def draw(self, screen):
        return
        
        
    def become_deactivated(self):
        return False
    
    def become_standby(self):
        self.manager.start_standby()
        return True
        
    def become_firing(self):
        return False
        

class StandbyCannon(ASprite):
    """State 2: keeps on left side of screen and follows player's vertical position
    
    Note: will probably be animated in the future; this doesn't change behavior"""
    
    def __init__(self, manager, target, sprite_filename):
        """manager is the base Cannon object
        target is the player's sprite
        """
    
        super(StandbyCannon, self).__init__(sprite_filename, 0)
    
        self.manager = manager
        self.target = target
        
        self.STATE_NUMBER = manager.STANDBY
        
        
    def update(self):
        """keep left, follow the target's vertical position"""
        
        self.rect.left = 0
        self.rect.centery = self.target.rect.centery
        
        
    def become_deactivated(self):
        self.manager.start_deactivated()
        return True
        
    def become_standby(self):
        return False
        
    def become_firing(self):
        self.manager.start_firing(self.rect.center)
        return True
        
        

class FiringCannon(ASprite):
    """State 3: moves in one direction (initially right) across screen
    
    Note: will probably be animated in the future; this doesn't change behavior"""
    
    def __init__(self, manager, position, sprite_filename, speed):
        """manager is the base Cannon object
        position is the sprite's initial rect.center coordinate
        """
        
        super(FiringCannon, self).__init__(sprite_filename, speed)
        
        self.manager = manager
        self.rect.center = position
        
        self.direction = EAST
        
        self.STATE_NUMBER = manager.FIRING
        
        
    def update(self):
        """move in the direction"""
        
        self.move(self.direction)
        
        if self.rect.left < 0 or self.rect.right >= options.width:
            self.become_deactivated()
            
            
    def set_direction(self, direction):
        self.direction = direction
            
            
    def become_deactivated(self):
        self.manager.start_deactivated()
        return True
        
    def become_standby(self):
        return False
        
    def become_firing(self):
        return False

