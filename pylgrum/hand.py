"""One player's hand."""

from pylgrum.card import Card
from pylgrum.stack import CardStack
from pylgrum.errors import OverdealtHandError

class Hand(CardStack):
    """A Hand represents the cards a player is holding.

    Hands generally have 10 cards, but can have 11 during a turn.
    """

    def add(self, newcard: Card):
        """Add a card to the hand (extends CardStack.add()).

        Raises OverdealtHandError if adding the card would make the hand
        size > 11.
        """
        if self.size() > 10:
            raise OverdealtHandError
        super().add(newcard)
