"""

yarsmanager.py

Contains the YarsManager class which is the GameManager for this game.

"""

import options
from gamestate import GameManager
from title import Title
from infoscreen import InfoScreen
from level import Level
from levelends import DeathAnimation, WinAnimation

class YarsManager(GameManager):
    """YarsManager is a GameManager which provides universal methods to change state.

    Following the original Yars' Revenge design, an intermediate screen showing
    score and lives will be displayed before the state we are transitioning to.
    """

    def __init__(self):
        GameManager.__init__(self, Title(self))

    
    def new_game(self):
        """initialize game variables (e.g. score, lives, energy)
        and prepare the first level
        """

        self.score = 0
        self.lives = options.initial_lives
        self.max_energy = options.max_energy
        self.energy = 0

        self.next_level()


    def game_over(self):
        """Go to intermediate screen then return to title
        """

        title_screen = Title(self)
        info_screen = InfoScreen(self, self.score, '', title_screen)
        self.change_state(info_screen)


    def next_level(self):
        """Go to intermediate screen then start next level
        """

        next_level = Level(self)
        info_screen = InfoScreen(self, self.score, self.lives, next_level)
        self.change_state(info_screen)


    def restart_level(self, next_level):
        """Go to intermediate screen then resume this level

        Note: Because some things are unchanged the level will be responsible
        for resetting its own status before calling this method.
        """

        self.reset_energy()
        next_level.reset_positions()
        info_screen = InfoScreen(self, self.score, self.lives, next_level)
        self.change_state(info_screen)


    def kill_player(self, next_level):
        """Player loses a life. If this leaves player with 0 lives, game over.
        Otherwise, restarts level
        """

        self.lives -= 1
        if self.lives == 0:
            self.game_over()
        else:
            self.restart_level(next_level)


    def give_life(self):
        """Player gains a life up to a maximum"""

        self.lives += 1


    def add_score(self, amount):
        """Increase score by given amount"""

        self.score += amount


    def give_energy(self, amount):
        """energy increases by the given amount"""

        self.energy += amount
        if self.energy > self.max_energy:
            self.energy = self.max_energy


    def spend_energy(self, amount):
        """energy decreases by the given amount if possible

        returns True if successful
        returns False if not enough energy; energy will be unchanged
        """

        if self.energy < amount:
            return False
        else:
            self.give_energy(-amount)
            return True
            
            
    def reset_energy(self):
        self.energy = 0
