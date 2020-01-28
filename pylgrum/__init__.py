"""PyLGRum is a set of classes implementating of the card game Gin Rummy in Python.

"PyLGRum" is an acronym for "Python Library for Gin Rummy".

For more details about the history, rules, and terminology of the game, see:
    https://en.wikipedia.org/wiki/Gin_rummy

Packages included:
    pylgrum: Core domain objects and base classes required to play a game.
    pylgrum.server: A game-coordinating class (GameManager).
    pylgrum.tui: A text UI game, functional as a proof of concept.

Classes in core `pylgrum` package:
    Card: a playing card w/ suit, rank (e.g. "queen"), and point value.
    CardStack: a collection of Cards.
    Sub-classed by:
        Deck: 52 unique Cards
        Meld: A (potentially partial) set or run of Cards
        Hand: Cards held by a given Player
    Game: A sequence of Moves between two Players
    Player: has a Hand, and implements hooks for the two phases of
        a Move
    Move: a stateful message passed between Game and Player that exchanges a
        Card and allows a Player to signal the end of the Game.

Note: this package uses PEP-484 style type annotations, and thus needs
python >=3.5.
"""
