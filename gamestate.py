"""

gamestate.py

Contains classes GameManager and GameState for implementing game states

"""

class GameManager():
    """GameManager is the universal accessor for GameStates.
    It contains methods for updating, event handling, drawing, and transitioning.
    """

    def __init__(self, state=None):
        self.change_state(state)

    def update(self):
        self.current_state.update()

    def handle_events(self, events, keys):
        return self.current_state.handle_events(events, keys)

    def draw(self, screen):
        self.current_state.draw(screen)

    def change_state(self, new_state):
        self.current_state = new_state

    def get_state(self):
        return self.current_state



class GameState():
    """GameState contains the behavior for one state.
    """

    def __init__(self, manager):
        self.manager = manager

    def update(self):
        """updates all sprites"""
        pass

    def handle_events(self, events, keys):
        """handles events and keypresses"""
        return True

    def draw(self, screen):
        """draws all sprites to the screen"""
        raise NotImplementedError
