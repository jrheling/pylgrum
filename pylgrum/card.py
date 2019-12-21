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

    Public methods:
     __init__(Suit, Rank)
     score_val() - returns point value for cards of that rank.
     same_suit(Card) - True if both cards share a suit
     same_rank(Card) - True if both cards share a rank
     is_same_card(Card) - True if suit and rank match
     overriden operators ==, !=, <, >, <=, >= work on point value
       (e.g. Jack == King)

    WARNING: it is arguably bad that "==" operates on point value as opposed
    to suit/rank. On the other hand, it might be strange if all comparison
    operators _other than_ "==" worked on point value, and "==" didn't.
    """
    rank = None # type: Rank
    suit = None # type: Suit

    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.suit = suit
        self.rank = rank

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
        """Return the point value of a card (if held as 'deadwood')."""
        if self.rank.name is "A":
            return 1
        elif self.rank.name in ("JACK", "QUEEN", "KING"):
            return 10
        else:
            return int(self.rank.value)

    def rank_val(self) -> int:
        """Return a sort-able rank value of the card.

        Note the differerence between rank_val and score_val: both JACK
        and TEN are worth 10 points score-wise, but JACK is an 11 in
        rank_val and TEN is a 10. rank_val is used to sort potential
        sets.
        """
        if self.rank.value == 'J':
            return 11
        elif self.rank.value == 'Q':
            return 12
        elif self.rank.value == 'K':
            return 13
        else:
            return int(self.rank.value)

    def same_suit(self, other) -> bool:
        """True if both cards share a suit."""
        if self.suit == other.suit:
            return True
        return False

    def same_rank(self, other) -> bool:
        """True if both cards share a rank."""
        if self.rank == other.rank:
            return True
        return False

    def is_same_card(self, other) -> bool:
        """Unlike ==, is_same_card() requires same rank + suit."""
        if self.same_suit(other) and self.same_rank(other):
            return True
        return False

    def __str__(self):
        rank_str = self.rank.name[0] + self.rank.name[1:].lower()
        suit_str = self.suit.name[0] + self.suit.name[1:].lower() + 's'
        return "{} of {}".format(rank_str, suit_str)

    def __hash__(self):
        return hash(self.rank) ^ hash(self.suit)
