"""A Meld is a set or run - this class tracks potential or complete melds."""

from pylgrum.card import Card
from pylgrum.stack import CardStack
from pylgrum.errors import InvalidMeldError

class Meld(CardStack):
    """Referenceable data-structure to store melds and potential melds.

    A complete *set* is three or more cards of the same Rank.
    A complete *run* is three or more cards of the same Suit with consecutive Ranks.

    Note: Melds are always sorted by rank value, so unlike their ancestors in
    the CardStack class tree, do not behave like stacks in all regards.

    Because this class stores _potential_ Melds, any single card is a valid
    meld.
    """

    def __init__(self, *cards: Card) -> None:
        """Create a new (potential) Meld with the specified cards.

        Args:
            *cards (Card): the cards to add to the Meld

        Raises InvalidMeldError if cards don't match in suit or rank.
        """

        self.all_same_rank = False # a potential set must be all the same rank
        self.all_same_suit = False # a potential run must be all the same suit
        self.is_run = False        # same suit, >=3 consecutively ranked cards
        self.is_set = False        # same rank, >=3 cards

        super().__init__()
        for card in [*cards]:
            super().add(card) # intentionally not calling our add(), since
                              #  here we want to accept or reject the whole
                              #  meld.

        try:
            self._update_validity()
        except InvalidMeldError:
            for i in reversed(range(0, self.size())):
                #print("removing card {} (len={})".format(i,len(self.cards)))
                self.remove(i)
            raise

    @property
    def complete(self) -> bool:
        """True for any full, valid Meld."""
        if self.is_run or self.is_set:
            return True
        return False

    def _update_validity(self) -> None:
        """Inspect a Meld for validity and potential completeness.

        A _valid_ meld is any meld that could become a full run or set. In
        order to be valid, then, a meld needs to either be all the same rank
        (if it's going to maybe become a set) or be all the same suit (if
        it has a chance of becoming a run).

        Valid melds may also be complete. Completeness requires at least 3
        cards and, in the case of runs, sequential continuity across all of
        them.

        Side effects:
         * updates all_same_suit and all_same_meld

        Raises InvalidMeldError.
        """
        self.all_same_suit = self._check_same_suit(*self.cards)
        self.all_same_rank = self._check_same_rank(*self.cards)

        if self.size() == 0:
            # empty meld is weird, but not impossible -- means there's
            #  nothing else to check
            self.is_set = False
            self.is_run = False
            return

        if not (self.all_same_rank or self.all_same_suit):
            raise InvalidMeldError("Proposed meld {} not ".format(self.cards)
                                   + "either all same "
                                   + "suit or same rank.")

        if self.all_same_rank:
            self.is_set = (self.size() >= 3)
        else:
            self.is_set = False

        if self.all_same_suit:
            if self.size() >= 3:
                # even though add() sorts, this is not redundant, because
                #   cards added on init() do not get sorted before the
                #   first call to _update_validity(). This may not be
                #   optimally self-evident, but it is the currently
                #   intended behavior.
                sorted_cards = sorted(self.cards,
                                      key=lambda card: card.rank_val())
                is_sequence = True
                for i in range(1, len(sorted_cards)):
                    if sorted_cards[i].rank_val() != (
                            sorted_cards[0].rank_val() + i):
                        is_sequence = False
                        break
                self.is_run = is_sequence
            else:
                self.is_run = False
        else:
            self.is_run = False

    @staticmethod
    def _check_same_suit(*cards) -> bool:
        """Return true iff all cards passed as argument are of the same suit."""
        cards = [*cards]
        if len(cards) > 0:
            reference_card = cards[0]
            for card in cards[1:]:
                if not reference_card.same_suit(card):
                    return False
            return True
        return False

    @staticmethod
    def _check_same_rank(*cards) -> bool:
        """Return true iff all cards passed as argument are of the same rank."""
        cards = [*cards]
        if len(cards) > 0:
            reference_card = cards[0]
            for card in cards[1:]:
                if not reference_card.same_rank(card):
                    return False
            return True
        return False

    def add(self, newcard: Card) -> None:
        """Add a card that fits the meld (extends CardStack.add()).

        Args:
            newcard (Card): the card to add

        Raises InvalidMeldError when non-fitting cards are attempted.
        """

        # allow the addition if either same suit or same rank remains true
        #  - in the case of adding a second card to a potential meld of one
        #  a single card, it will necessarily be the case that one of
        #  is_run or is_set becomes False. This is OK, as long
        #  as one remains True.
        if not (self._check_same_suit(*self.cards, newcard) or
                self._check_same_rank(*self.cards, newcard)):
            raise InvalidMeldError("Adding {} ".format(newcard)
                                   + "to meld with {} ".format(self.cards)
                                   + "would leave it invalid.")
        super().add(newcard)
        self.cards.sort(key=lambda card: card.rank_val())
        self._update_validity()

    def remove(self, i: int) -> Card:
        """Remove a card from the meld (extends CardStack.remove()).

        Args:
            i (int): index of the card to be removed.

        Raises CardNotFoundError
        """
        super().remove(i)
        self._update_validity()
