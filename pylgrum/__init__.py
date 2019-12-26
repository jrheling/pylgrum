"""PyLGRum: Python Learning Gin Rummy

PyLGRum is an implementation of the card game Gin Rummy in Python.

For more details about the game history and rules, see:
    https://en.wikipedia.org/wiki/Gin_rummy

Primary classes:

- Card: a playing card w/ suit, rank (e.g. "queen"), and point value.
- CardStack: a collection of Cards.
    - Deck: 52 unique Cards
    - Meld: a (potentially partial) set or run of Cards
    - Hand: Cards held by a given Player
        - HandWithMelds: a Hand organized by (potentially partial) Melds
- Game: a sequence of Moves between two Players. Moves are passed between the
  Players and Game.
    - TUIGame: simple console-based PoC
- Move: a stateful message passed between Game and Player that exchanges a
  Card and allows a Player to signal the end of the Game.
- Player (abstract): has a Hand, and implements hooks for the two phases of
  a Move.
    - TUIPlayer: simple console-based PoC

Note: this package uses PEP-484 style type annotations, and thus needs
python >=3.5.
"""

#pylint: disable=wildcard-import
from .card import *
from .stack import *
from .errors import *
from .deck import *
from .hand import *
from .game import *
from .player import *
from .move import *
from .meld import *
from .hand_melds import *
from .tui_player import *
from .tui_game import *
from .pylgrum_server import *

__all__ = ['Suit', 'Rank', 'Card', 'CardStack', 'PylgrumError',
           'CardNotFoundError', 'Deck', 'Player']
