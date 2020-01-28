"""A standard 52-card deck of cards."""

from pylgrum.card import Card, Rank, Suit
from pylgrum.stack import CardStack

class Deck(CardStack):
    """A deck has 52 cards in 4 suits (no jokers)."""

    def __init__(self):
        """Create a new Deck."""
        super().__init__()
        for rank in list(Rank):
            for suit in list(Suit):
                self.add(Card(rank=rank, suit=suit))
