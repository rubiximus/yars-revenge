"""

cannon.py

The cannon is the player's special weapon, notable for being the only way to
destroy the enemy base. Its behavior is split into three states:

1. Deactivated (no image or behavior)
2. Standby (visible on right side of screen; follows player's vertical position)
3. Firing across the screen (rightwards)
4. Returning across the screen (leftwards)

This behavior is implemented as a state machine. Cannon is the state manager,
DeactivatedCannon is state 1, StandbyCannon is state 2, FiringCannon is state 3,
and ReturningCannon is state 4.

"""

from pygame import Surface, Rect
from pygame.sprite import Sprite
from pygame.mask import Mask

from statemachine import Manager, State
from asprite import ASprite
import vector
import options

class Cannon(Manager):
    """State manager for the cannon
    
    Contains class constants DEACTIVATED, STANDBY, FIRING, and RETURNING which are the
    state numbers for the corresponding states."""
    
    DEACTIVATED = 1
    STANDBY = 2
    FIRING = 3
    RETURNING = 4
    
    def __init__(self, deactivated_args, standby_args, firing_args, target):
        """*_args are tuples of arguments; see corresponding classes' __init__()
        target is the player's sprite (the sprite to follow on standby)
        """
        
        Manager.__init__(self)

        self.deactivated_args = deactivated_args
        self.standby_args = standby_args
        self.firing_args = firing_args
        
        self.target = target
        
        self.start_deactivated()

        self.update_sprite_attributes()
        
        
    def start_deactivated(self):
        deactive = DeactivatedCannon(self, *self.deactivated_args)
        self.change_state(deactive)

        
    def start_standby(self):
        standby = StandbyCannon(self, self.target, *self.standby_args)
        self.change_state(standby)

        
    def start_firing(self, position):
        firing = FiringCannon(self, position, *self.firing_args)
        self.change_state(firing)


    def start_returning(self, position):
        returning = ReturningCannon(self, position, *self.firing_args)
        self.change_state(returning)

        
        
class DeactivatedCannon(State):
    """State 1: no image or behavior. All functions do nothing. Pretty simple.
    
    For collision simplification this class is an empty sprite with
    image and rect of zero area.
    """
    
    def __init__(self, manager):
        State.__init__(self, manager)
        
        self.sprite = Sprite()
        self.sprite.image = Surface((0, 0))
        self.sprite.rect = Rect(0, 0, 1, options.height)
        self.sprite.mask = Mask((1, options.height))
        self.sprite.mask.fill()
        
        self.STATE_NUMBER = manager.DEACTIVATED
        
        
    def transition_to(self, new_state_number):
        if new_state_number == self.manager.STANDBY:
            self.manager.start_standby()
            return True

        return False



class StandbyCannon(State):
    """State 2: keeps on left side of screen and follows player's vertical position
    
    Note: will probably be animated in the future; this doesn't change behavior"""
    
    def __init__(self, manager, target, sprite_filename):
        """manager is the base Cannon object
        target is the player's sprite
        """
    
        State.__init__(self, manager)
        
        self.sprite = ASprite(sprite_filename, 0)
        self.target = target
        self.STATE_NUMBER = manager.STANDBY
        
        
    def update(self):
        """keep left, follow the target's vertical position"""
        
        self.sprite.rect.left = 0
        self.sprite.rect.centery = self.target.rect.centery
        
    
    def transition_to(self, new_state_number):
        if new_state_number == self.manager.DEACTIVATED:
            self.manager.start_deactivated()
            return True

        if new_state_number == self.manager.FIRING:
            self.manager.start_firing(self.sprite.rect.center)
            return True

        return False



class FiringCannon(State):
    """State 3: moves in one direction (initially right) across screen
    
    Note: will probably be animated in the future; this doesn't change behavior"""
    
    def __init__(self, manager, position, sprite_filename, speed):
        """manager is the base Cannon object
        position is the sprite's initial rect.center coordinate
        """
        
        State.__init__(self, manager)

        self.sprite = ASprite(sprite_filename, speed)
        self.sprite.rect.center = position
        self.direction = vector.EAST
        
        self.STATE_NUMBER = manager.FIRING
        
        
    def update(self):
        """move in the direction"""
        
        self.sprite.move(self.direction)
        
        rect = self.sprite.rect
        if rect.left < 0 or rect.right >= options.width:
            self.transition_to(self.manager.DEACTIVATED)
            
            
    def transition_to(self, new_state_number):
        if new_state_number == self.manager.DEACTIVATED:
            self.manager.start_deactivated()
            return True

        if new_state_number == self.manager.RETURNING:
            self.manager.start_returning(self.sprite.rect.center)
            return True

        return False



class ReturningCannon(FiringCannon):
    """State 4: moves right across the screen
    
    Currently just a FiringCannon with different direction and state_number"""

    def __init__(self, manager, position, sprite_filename, speed):
        FiringCannon.__init__(self, manager, position, sprite_filename, speed)

        self.direction = vector.WEST
        
        self.STATE_NUMBER = manager.RETURNING
