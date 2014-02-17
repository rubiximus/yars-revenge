"""

yarsmanager.py

Contains the YarsManager class which is the GameManager for this game.

"""

import options
from gamestate import GameManager
from title import Title
from infoscreen import InfoScreen
from level import Level

class YarsManager(GameManager):
    """YarsManager is a GameManager which provides universal methods to change state.

    Following the original Yars' Revenge design, an intermediate screen showing
    score and lives will be displayed before the state we are transitioning to.
    """

    def __init__(self):
        super(YarsManager, self).__init__(Title(self))

    
    def new_game(self):
        """initialize game variables (e.g. score, lives)
        and prepare the first level
        """

        self.score = 0
        self.lives = options.initial_lives

        self.next_level()


    def game_over(self):
        """Go to intermediate screen then return to title
        """

        game_over_state = Title(self)
        self.change_state(game_over_state)


    def next_level(self):
        """Go to intermediate screen then start next level
        """

        next_level = Level(self)
        info_screen = InfoScreen(self, self.score, self.lives, next_level)
        self.change_state(info_screen)


    def restart_level(self):
        """Go to intermediate screen then resume this level

        Note: Because some things are unchanged the level will be responsible
        for resetting its own status.
        """

        pass
