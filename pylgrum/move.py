"""Represents a single move in a game.

The Move object is prepared by the Player, then submitted to the Game for
execution, and returned from the Game to the Player completed.
"""
from enum import Enum

from pylgrum.errors import IllegalMoveError
from pylgrum.card import Card

class MoveState(Enum):
    """Tracks the state of a given move."""
    NEW = 1
    IN_PROGRESS = 2
    COMPLETE = 3

class CardSource(Enum):
    """Describes where a Card acquired in a Move is taken from."""
    DRAW_STACK = 1
    DISCARD_STACK = 2

class Move():
    """A Move tracks cards acquired/discarded in a single turn in a game.

    The combination of initial hand states and discard and sequence of moves
    should be sufficient to re-create the game as perceived by either player.
    """

    def __init__(self, available_discard: Card) -> None:
        """Create and initialize new Move.

        Args:
            available_discard (Card): the card showing on top of the discard pile
        """
        self.state = MoveState.NEW
        self.available_discard = available_discard
        self.card_source = None  # CardSource
        """Indicate if new card is to come from the draw or discard pile."""
        self.acquired = None     # Card
        """The card added to a player's hand during the move."""
        self.discarded = None   # Card
        """The card discarded by the player during the move."""
        self.knocking = False
        """Set to True when the player is ending the game ("knocking")."""

    def choose_card_from_draw(self) -> None:
        """Configure the Move to take a card from the draw pile."""
        if self.card_source is not None:
            raise IllegalMoveError("Asked to draw after already drawing or taking the discard.")
        self.card_source = CardSource.DRAW_STACK
        self.state = MoveState.IN_PROGRESS

    def choose_card_from_discard(self) -> None:
        """Configure the Move to take a card from the discard pile."""
        if self.card_source is not None:
            raise IllegalMoveError("Asked to draw discard after already "
                                   + "drawing or taking the discard.")
        self.card_source = CardSource.DISCARD_STACK
        self.state = MoveState.IN_PROGRESS

    def discard(self, discarded: Card) -> None:
        """Identify the card that will be discarded to finish this move.

        Args:
            discarded (Card): the card to be discarded
        """
        if self.state != MoveState.IN_PROGRESS:
            raise IllegalMoveError("Can't discard from state {}".format(
                self.state))
        if self.discarded is not None:
            raise IllegalMoveError(
                "Unexpectedly non-None discarded card in discard()")
        self.discarded = discarded
        self.state = MoveState.COMPLETE

    def __str__(self):
        if self.state != MoveState.COMPLETE:
            return "(move still in progress)"
        return "Took {} from {} and discarded {}".format(
            self.acquired,
            self.card_source,
            self.discarded)

    def public_str(self):
        """Show summary of move that doesn't reveal player-private details.

        If a player took a discard, it's fair for their opponent to see what
        the card was. But if a player drew from the draw stack, the opponent
        does not know what card was drawn.
        """
        if self.card_source == CardSource.DISCARD_STACK:
            source = "discard"
            card = self.acquired
        elif self.card_source == CardSource.DRAW_STACK:
            source = "draw"
            card = "a card"

        return "Took {} from the {} pile and discarded {}".format(
            card, source, self.discarded)
