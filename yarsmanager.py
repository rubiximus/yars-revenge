"""

yarsmanager.py

Contains the YarsManager class which is the GameManager for this game.

"""

import options
from gamestate import GameManager
from level import Level

class YarsManager(GameManager):
    """YarsManager is a GameManager which provides universal methods to change state.

    Following the original Yars' Revenge design, an intermediate screen showing
    score and lives will be displayed before the state we are transitioning to.
    """

    def __init__(self):
        super(YarsManager, self).__init__(Level(self))

    
    def game_over(self):
        """Go to intermediate screen then return to title
        """

        game_over_state = None


        pass


    def next_level(self):
        """Go to intermediate screen then start next level
        """

        next_level = None

        pass


    def restart_level(self):
        """Go to intermediate screen then resume this level

        Note: Because some things are unchanged the level will be responsible
        for resetting its own status.
        """

        pass
