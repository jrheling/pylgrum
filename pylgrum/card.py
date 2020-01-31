"""Implementation of Card class, and supporting enums Rank and Suit."""

from enum import Enum

class Rank(Enum):
    """Trivial enum of card ranks (e.g. ace, face cards, royals, etc.)."""
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Suit(Enum):
    """Trivial enum of card suits.

    Comparison uses bridge-style suit rankings:
        Spade > Heart > Club > Diamond
    """
    SPADE = 4
    HEART = 3
    CLUB = 2
    DIAMOND = 1

class Card:
    """Cards have suit+rank, point value, and can be compared (by point value).

    Attributes:
        rank (Rank): the face value of the card (Ace, 2..10, Jack, Queen, King)
        suit (Suit): the suit of the card (Heart, Club, Spade, Diamond)

    In addition to Rank, Cards have a point value that maps the Rank to the
    effect the card has on scoring in Gin Rummy (e.g. both Jack and King are
    worth 10 points).

    Card comparisons are done first on suit and then on rank. To evaluate cards
    based on points as deadwood, use score_val()
    """

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """Create a new Card.

        Args:
            rank (Rank): the new Card's rank
            suit (Suit): the suit of the new card
        """
        self.suit: Suit = suit
        self.rank: Rank = rank

    @classmethod
    def from_text(cls, *card_strings):
        """Return a new Card from a string XY, where X indicates rank and Y suit.

        Args:
            card_strings (str): the encoded rank/suit of the card to create

        For example, "3H" creates a 3 of Hearts, "AC" an Ace of Clubs, etc.
        """
        face_cards = {
            'A': 1,
            'J': 11,
            'Q': 12,
            'K': 13
        }
        suits = {
            'S': 'SPADE',
            'H': 'HEART',
            'C': 'CLUB',
            'D': 'DIAMOND'
        }

        new_cards = []
        for text in card_strings:
            rank_char = text[:1]
            try:
                rank = Rank(int(rank_char))
            except ValueError:
                # here for A, J, Q, K
                rank = Rank(face_cards[rank_char])

            suit_char = text[1:]
            suit = Suit[suits[suit_char]]

            new_cards.append(Card(rank=rank, suit=suit))

        if len(new_cards) == 1:
            return new_cards[0]
        elif len(new_cards) > 1:
            return new_cards

    def __eq__(self, other) -> bool:
        return (self.suit.value == other.suit.value and
                self.rank.value == other.rank.value)

    def __ne__(self, other) -> bool:
        return (self.suit.value != other.suit.value or
                self.rank.value != other.rank.value)

    def __lt__(self, other) -> bool:
        if self.suit.value < other.suit.value:
            return True
        elif self.suit.value == other.suit.value:
            return self.rank.value < other.rank.value
        else:
            return False

    def __le__(self, other) -> bool:
        if self.suit.value <= other.suit.value:
            return True
        elif self.suit.value == other.suit.value:
            return self.rank.value <= other.rank.value
        else:
            return False

    def __gt__(self, other) -> bool:
        if self.suit.value > other.suit.value:
            return True
        elif self.suit.value == other.suit.value:
            return self.rank.value > other.rank.value
        else:
            return False

    def __ge__(self, other) -> bool:
        if self.suit.value >= other.suit.value:
            return True
        elif self.suit.value == other.suit.value:
            return self.rank.value >= other.rank.value
        else:
            return False

    def __hash__(self):
        return hash(self.rank) ^ hash(self.suit)

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
        return self.rank.value

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

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        rank_val = self.rank.value
        if rank_val > 1 and rank_val < 11:
            rank_str = self.rank.value
        elif rank_val == 1:
            rank_str = 'A'
        elif rank_val == 11:
            rank_str = 'J'
        elif rank_val == 12:
            rank_str = 'Q'
        elif rank_val == 13:
            rank_str = 'K'
        suit_str = self.suit.name[0]
        return "{}{}".format(rank_str, suit_str)

    @property
    def long_name(self):
        rank_str = self.rank.name[0] + self.rank.name[1:].lower()
        suit_str = self.suit.name[0] + self.suit.name[1:].lower() + 's'
        return "{} of {}".format(rank_str, suit_str)

