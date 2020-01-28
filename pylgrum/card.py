"""Implementation of Card class, and supporting enums Rank and Suit."""

from enum import Enum

class Rank(Enum):
    """Trivial enum of card ranks (e.g. ace, face cards, royals, etc.)."""
    ACE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'

class Suit(Enum):
    """Trivial enum of card suits."""
    SPADE = 'S'
    HEART = 'H'
    CLUB = 'C'
    DIAMOND = 'D'

class Card:
    """Cards have suit+rank, point value, and can be compared (by point value).

    Attributes:
        rank (Rank): the face value of the card (Ace, 2..10, Jack, Queen, King)
        suit (Suit): the suit of the card (Heart, Club, Spade, Diamond)

    In addition to Rank, Cards have a point value that maps the Rank to the
    effect the card has on scoring in Gin Rummy (e.g. boht Jack and King are
    worth 10 points).

    This class overrides basic comparison operators with regard to point value,
    *not* Rank.

    WARNING: it is arguably bad that "==" operates on point value as opposed
    to suit/rank. On the other hand, it might be strange if all comparison
    operators _other than_ "==" worked on point value, and "==" didn't.
    """

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """Create a new Card.

        Args:
            rank (Rank): the new Card's rank
            suit (Suit): the suit of the new card
        """
        self.suit: Suit = suit
        self.rank: Rank = rank

    def __eq__(self, other) -> bool:
        return self.score_val() == other.score_val()

    def __ne__(self, other) -> bool:
        return self.score_val() != other.score_val()

    def __lt__(self, other) -> bool:
        return self.score_val() < other.score_val()

    def __le__(self, other) -> bool:
        return self.score_val() <= other.score_val()

    def __gt__(self, other) -> bool:
        return self.score_val() > other.score_val()

    def __ge__(self, other) -> bool:
        return self.score_val() >= other.score_val()

    def score_val(self) -> int:
        """Return the point value of a card."""
        val = None
        if self.rank == Rank.ACE:
            val = 1
        elif self.rank in (Rank.JACK, Rank.QUEEN, Rank.KING):
            val = 10
        else:
            val = int(self.rank.value)
        return val

    def rank_val(self) -> int:
        """Return a sort-able rank value of the card.

        Note the differerence between rank_val and score_val: both JACK
        and TEN are worth 10 points score-wise, but JACK is an 11 in
        rank_val and TEN is a 10. rank_val is used to sort potential
        sets.
        """
        val = None
        if self.rank == Rank.JACK:
            val = 11
        elif self.rank == Rank.QUEEN:
            val = 12
        elif self.rank == Rank.KING:
            val = 13
        else:
            val = int(self.rank.value)
        return val

    def same_suit(self, other) -> bool:
        """Compare card with another and return true if both have the same suit.

        Args:
            other (Card): the card to compare
        """
        if self.suit == other.suit:
            return True
        return False

    def same_rank(self, other) -> bool:
        """Compare card with another and return true if both have the same rank.

        Args:
            other (Card): the card to compare
        """
        if self.rank == other.rank:
            return True
        return False

    def is_same_card(self, other) -> bool:
        """Compare card with another and return true if theyq have the rank and suit.

        Args:
            other (Card): the card to compare

        Note: also see overridden == operator.
        """
        if self.same_suit(other) and self.same_rank(other):
            return True
        return False

    def __str__(self):
        rank_str = self.rank.name[0] + self.rank.name[1:].lower()
        suit_str = self.suit.name[0] + self.suit.name[1:].lower() + 's'
        return "{} of {}".format(rank_str, suit_str)

    def __hash__(self):
        return hash(self.rank) ^ hash(self.suit)
