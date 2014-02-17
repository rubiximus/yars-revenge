"""

statemachine.py

Contains the classes Manager and State for implementing state machine sprites.

"""

import pygame
from pygame.sprite import Sprite

class Manager(Sprite):
    """Manager is a Sprite which serves as a universal accessor for the states.
    It contains integer constants for identifying the states as well as the methods
    for updating, drawing and transitioning.

    Children of Manager will need to implement the transition function
    """

    #default state number; means that the manager does not have an active state
    STATELESS = -1

    def __init(self):
        super(Manager, self).__init__()

        self.current_state = None
        self.rect = None
        self.image = None
        self.mask = None


    def update(self):
        if self.current_state is None: return

        self.current_state.update()
        self.update_sprite_attributes()


    def update_sprite_attributes(self):
        """updates image, rect, and mask to those of the current state
        """

        self.image = self.current_state.get_image()
        self.rect = self.current_state.get_rect()
        self.mask = self.current_state.get_mask()


    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def start_transition(self, new_state_number):
        """causes the current state to transition to the state
        corresponding to new_state_number
        """
        
        return self.current_state.transition_to(new_state_number)


    def change_state(self, new_state):
        self.current_state = new_state
        self.update_sprite_attributes()
    

    def get_state(self):
        return self.current_state
    

    def get_state_number(self):
        """Returns a number corresponding to the current state.
        """
        
        return self.current_state.STATE_NUMBER


    def get_rect(self):
        return self.rect



class State():
    """State contains the behavior of one state as well as
    that state's rules for transitioning to other states.

    Note: State.sprite is the actual Sprite being drawn,
    but most behavior will be handled within State
    """

    def __init__(self, manager):
        super(State, self).__init__()

        self.manager = manager

        self.sprite = None
        self.state_number = Manager.STATELESS


    def update(self):
        pass


    def get_rect(self):
        if self.sprite is None: return None
        return self.sprite.rect


    def get_image(self):
        if self.sprite is None: return None
        return self.sprite.image


    def get_mask(self):
        if self.sprite is None: return None
        return self.sprite.mask

    
    def transition_to(self, new_state_number):
        """Contains the state's transition rules and behavior. This will generally
        involve calling some method in the Manager to start the new state.

        returns True if the transition to new_state_number's state is allowed
        otherwise returns False
        """

        return False
