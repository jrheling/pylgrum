"""Text-mode game controller."""
import time

from pylgrum import Game, Player
from pylgrum.tui_util import clear_screen

DELAY = 0.25 # in seconds

class TUIGame(Game):
    """Sub-class of Game, intended for use in console-based game.

    This class is appropriate for games with 1 or 2 human players
    interacting via text mode."""

    def __init__(self, p1: Player, p2: Player) -> None:
        print("Starting new game between {} and {}".format(p1, p2))

        print("Shuffling...")
        time.sleep(DELAY)
        print("Dealing...")
        time.sleep(DELAY)

        super().__init__(p1, p2)

    def pre_turn_hook(self):
        print("\nNext move is to {}".format(self._current_player))
        # print("Top of discard pile: {}".
        #       format(self._current_move.available_discard))
        input(" * * Press any key when {} is ready to play * *".
              format(self._current_player))

    def post_turn_hook(self):
        clear_screen()
        print("{}'s move:\n  {}".
              format(self._current_player, self._current_move.public_str()))
