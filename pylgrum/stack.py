"""The CardStack class implements a basic collection of Cards."""
import random

from itertools import groupby, cycle
from collections.abc import Iterable

from pylgrum.card import Card
from pylgrum.errors import CardNotFoundError

class CardStack():
    """A base class for collections of cards (e.g. deck, hand, discard pile).

    CardStack supports basic operations on collections of cards. In order to
    maintain generality, CardStack allows duplicates of a given card.

    No constraints on the contents of the CardStack are enforced by this base
    class, but common operations are implemented.

    The "top" of the stack is the end of the list.

    Public methods:
     add(c)      : adds c to the top of stack
     size()      : number of cards in the stack
     remove(i)   : removes and returns the card a given index
     find(c)     : searches the stack for c
     draw(c)     : removes and returns the "top" card in the stack
     shuffle()   : re-orders cards in the stack
     __eq__()    : stacks are equal iff they have the same cards
                   in the same order
     __str__()

    """

    def __init__(self) -> None:
        """Create a new CardStack."""
        self._cards = [] # List[Card]

    @property
    def cards(self) -> list:
        """The list of Cards in the stack.

        The caller should not modify the returned list.
        """
        return self._cards

    def size(self) -> int:
        """Return the number of cards in the stack."""
        return len(self._cards)

    def add(self, newcard: Card) -> None: # FIXME this type annotation is wrong
        """Add card(s) to the top of the stack.

        Args:
            newcard (Card): the Card to add, or a list of Cards
        """
        if isinstance(newcard, Iterable) and isinstance(newcard[0], Card):
            for card in newcard:
                self.add(card)
        elif isinstance(newcard, Card):
            self._cards.append(newcard)
        else:
            raise TypeError

    def remove(self, i: int) -> Card:
        """Remove and return the card at the given index.

        Args:
            i (int): the index of the Card to remove

        Raises: CardNotFoundError
        """
        try:
            target_card = self._cards[i]
        except IndexError:
            raise CardNotFoundError("Index value {} out of range".format(i))
        before_the_card = self._cards[0:i]
        after_the_card = self._cards[i+1:]
        self._cards = before_the_card + after_the_card
        return target_card

    def get(self, i: int) -> Card:
        """Return the card at the given index.

        Args:
            i (int): the index of the card to remove

        Raises: CardNotFoundError (if specified index is not in the stack)
        """
        try:
            target_card = self._cards[i]
        except IndexError:
            raise CardNotFoundError("Index value {} out of range".format(i))
        return target_card


    def find(self, targetcard: Card) -> int:
        """Search the stack for a specified card and return its index.

        Args:
            c (Card): the card to search for

        Raises:
            CardNotFoundError (if specified card is not in the stack)
        """
        for (position, checked_card) in enumerate(self._cards):
            if checked_card.is_same_card(targetcard):
                return position
        raise CardNotFoundError("{} not found in stack".format(
            targetcard.__str__()))

    def draw(self) -> Card:
        """Remove and return the top card on the stack."""
        if len(self._cards) < 1:
            raise CardNotFoundError("Empty stack.")
        return self._cards.pop()

    def peek(self) -> Card:
        """Return but do not remove the top card on the stack."""
        if len(self._cards) < 1:
            raise CardNotFoundError("Empty stack.")
        return self._cards[len(self._cards)-1]

    def shuffle(self) -> None:
        """Randomly re-order the stack."""
        random.shuffle(self._cards)

    def __eq__(self, other: 'card.CardStack') -> bool:
        """True iff both stacks have the same cards in the same order.

        Args:
            other (CardStack): the CardStack to compare
        """
        return self._cards == other.cards

    def __str__(self) -> str:
        """Printing a stack returns its cards in top-to-bottom order.

        Note: this will be the opposite of the list order - i.e. index 0
        is the last card listed. This way the visible order corresponds to the
        human notion of the "top" of the stack.
        """
        cards_to_print = self._cards.copy()
        cards_to_print.reverse()
        r_str = ", ".join([c.__str__() for c in cards_to_print])
        return r_str

    def group_by_suit(self):
        """Yield a list of cards of each suit.

        Note: works on a copy of the input (so we can sort by suit without
        expecting the caller to have done so and without modifying input).
        """
        sorted_by_suit = sorted(self._cards, key=lambda card: card.suit.value)

        grouped_by_suit = groupby(
            sorted_by_suit,
            key=lambda card: card.suit
        )
        for _, suit_group in grouped_by_suit:
            yield list(suit_group)

    @staticmethod
    def get_all_sequences(input_cards):
        """Yield a tuple for each sequence of consecutively-ranked cards.

        Args:
            input_cards (iterable of Card): cards in which to find sequences

        Note: this only looks for sequences of consecutively-ranked cards,
        without regard for suit. To limit by suit, call group_by_suit() first
        and then pass its output to this method.
        """
        sorted_by_rank = sorted(input_cards, key=lambda card: card.rank.value)

        temp_list = cycle(sorted_by_rank)
        next(temp_list)
        groups = groupby(
            sorted_by_rank,
            key=lambda card: card.rank.value+1 == next(temp_list).rank.value
        )
        for k, v in groups:
            if k:
                yield tuple(v) + (next((next(groups)[1])), )
