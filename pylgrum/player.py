"""One player in a game of GinRummy."""

from pylgrum.move import Move
from pylgrum import Hand, Card, PylgrumError, PylgrumInternalError
from pylgrum import game

class Player():
    """Abstract base class for a player in a Gin Rummy game.

    Subclasses must implement play().
    """

    def __init__(self, contestant_id: str = None, handtype: type = None):
        """Create a new player using the [optionally] specified type of Hand."""
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
        if not game:
            raise PylgrumError("Can't join game with None value")
        self.game = game

    def receive_card(self, card: Card) -> None:
        """Adds a card to the hand."""
        self.hand.add(card)

    def turn_start(self, move: Move) -> None:
        """Called by a Game to begin a turn.

        A move involves adding either the discard or the top of the draw
        pile to the Player's hand, then discarding.

        This method handles the first part of that process, and returns
        an in-progress Move to the Game for execution. The returned Move
        must specify the card source (draw or discard pile) the Player has
        chosen.

        Note that while the last-discarded card is passed as an argument
        to this method, that is only as a convenience. If the Player wants
        the discard, they do not directly "take" it from the argument here,
        but rather return a Move with card_source==DISCARD_STACK.
        """
        pass

    def turn_finish(self, move: Move) -> None:
        """Called by a Game to finish a turn.

        Before calling this method, the Game will have provided
        whatever Card the Player is acquiring on this turn via the Move.

        Before returning from this method the Player must identify their
        discard and populate it in the Move.

        If the player is "knocking" (finishing the game) they also must
        indicate that in the Move object before returning.

        Move state should be COMPLETE when this method returns.
        """
        pass


