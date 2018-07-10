"""One player in a game of GinRummy."""

from pylgrum import Hand, Card

class Player():
    """Abstract base class for a player in a Gin Rummy game.

    Subclasses must implement play().
    """

    def __init__(self):
        self._game = None
        self._hand = Hand()

    def join_game(self, game: 'Game'):
        ## FUTURE NOTE: as of 3.7, this should be able to be better done
        ##   with a "from __future__ import ..." statement
        self._game = game

    def receive_card(self, card: Card) -> None:
        """Adds a card to the hand."""
        self._hand.add(card)

    def play(self, discard: Card) -> (Card, bool):
        """Called by a Game to execute a single move.

        A move involves adding either the discard or the top of the draw
        pile to the Player's hand, then discarding. In the case that the
        Player "knocks" (ends the game), the discard is optional.

        play() must return a tuple consisting of:
         * Card or None. If supplied, the Card is the Player's discard
           from this move.
         * A boolean indicating whether the player is "knocking" to indicate
           that the game is over.

        Note that while the last-discarded card is passed as an argument
        to this method, that is only as a convenience. If a player wants to
        take the latest discard, they need to call Game.draw_discard().

        FIXME: need to define convention for asserting melds and deadwood
        """
        pass
