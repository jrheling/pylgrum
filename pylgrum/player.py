"""One player in a game of GinRummy."""

from pylgrum.card import Card
from pylgrum.hand import Hand
from pylgrum.move import Move
from pylgrum.errors import PylgrumError, PylgrumInternalError

class Player():
    """Abstract base class for a player in a Gin Rummy game.

    Subclasses must implement play().
    """

    def __init__(self, contestant_id: str = None, handtype: type = None):
        """Create a new Player using the [optionally] specified type of Hand.

        Args:
            contestant_id (str): [optional] ID value of the entity operating
                this player
            handtype (Hand subclass): [optional] Allows Hand classes with
                different behaviors (e.g. HandWithMelds) to be used by Player
        """
        self.game = None
        self.contestant_id = contestant_id
        if handtype is None:
            self.hand = Hand()
        else:
            if issubclass(handtype, Hand):
                self.hand = handtype()
            else:
                raise PylgrumInternalError("Type {} is not a ".format(handtype)
                                           + "subclass of Hand.")

    def join_game(self, game: 'game.Game'):
        """Join player to a game."""
        if not game:
            raise PylgrumError("Can't join game with None value")
        self.game = game

    def receive_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.hand.add(card)

    def turn_start(self, move: Move) -> None:
        """Called by a Game to begin a turn. (abstract)

        Args:
            move (Move): the Move object used to hold/transfer move details

        A move involves adding either the discard or the top of the draw
        pile to the player's hand, then discarding.

        This method handles the first part of that process, and populates
        the in-progress move with details that the game will execute. After
        this call, the Move must specify the card source (draw or discard
        pile) that the player has chosen.

        Note that while the last-discarded card is passed as an argument
        to this method, that is only as a convenience. If the player wants
        the discard, they do not directly "take" it from the argument here,
        but rather set a move with card_source==DISCARD_STACK.
        """

    def turn_finish(self, move: Move) -> None:
        """Called by a Game to finish a turn. (abstract)

        Args:
            move (Move): the Move object used to hold/transfer move details

        Before calling this method, the game will have provided
        whatever card the player is acquiring on this turn via the move.

        Before returning from this method the player must identify their
        discard and populate it in the move.

        If the player is "knocking" (finishing the game) they also must
        indicate that in the move object before returning.

        Move state should be COMPLETE when this method returns.
        """
