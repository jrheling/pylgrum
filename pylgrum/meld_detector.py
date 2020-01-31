"""Hand subclass that finds the best melds in a set of cards."""

from itertools import cycle, groupby

from pylgrum.hand import Hand
from pylgrum.card import Card, Suit, Rank
from pylgrum.hand_melds import HandWithMelds

class MeldDetector(HandWithMelds):
    """MeldDetector finds the optimal set of melds within a hand.

    This is used by the Game to confirm validity of a win claimed by a player,
    but can also be used by various player classes to either provide hints to a
    human player or to drive optimal play by machine players.

    **IMPORTANT NOTE** MeldDetector breaks the guarantee some of its class
    ancestors make about card ordering. Order of cards is not guaranteed, and
    will change at runtime depending on other methods called.

    For that reason, inherited methods that only make sense if card order is
    stable will raise
    """

    def __init__(self, *cards) -> None:
        """Create a MeldDetector, optionally initialized from a set of cards.

        Args:
            hand (Hand): [optional] hand to initialize from

        If provided, the cards the MeldDetector examines will be initialized
        to match the contents of the provided Hand.
        """
        super().__init__()
        for card in [*cards]:
            self.add(card)

        # flag used to indicate if detection has been done - cleared when the
        #  underlying card stack changes such that we need to re-dectect
        self._detected = False

    @property
    def cards(self):
        """Return a set with the cards in this hand.

        Ancestor classes return a list, but our order is unstable.
        """
        return set(self._cards)

    # These do not make sense for HandDetector instances, and will not behave
    # in a useful, reliable, or helpful way. Make that clear by raising
    def remove(self, i: int):
        # no use case for this yet, but if needed it could be implemented as a
        #  combination of super().find() and super().remove()
        raise NotImplementedError

    def get(self, i: int):
        raise NotImplementedError

    def find(self, c: Card):       # parent method returns an index
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def peek(self, i: int):        # "top" of stack is meaningless here
        raise NotImplementedError

    # The following methods all simply wrap their superclass implementations for
    #  the purpose of unsetting our _detected flag.
    def add(self, newcard: Card) -> None:
        """Extends base method to add a card to the hand."""
        super().add(newcard)
        self._sort_cards()

    def _sort_cards(self) -> None:
        """Sort the cards by suit then rank."""
        self._detected = False
        self._cards.sort()

    @property
    def deadwood_count(self) -> int:
        """Number of cards in the hand that aren't in a meld."""
        self._detect_all_melds()
        deadwood_count = 0
        for card in self.cards:
            if self.melds_using_card(card) is None:
                deadwood_count += 1
        return deadwood_count

    @property
    def deadwood_value(self) -> int:
        """Total value of cards in the hand that aren't in a meld."""
        self._detect_all_melds()
        deadwood_val = 0
        for card in self.cards:
            if self.melds_using_card(card) is None:
                deadwood_val += card.score_val()
        return deadwood_val

    def _detect_all_melds(self) -> None:
        """Compute all complete melds in the hand.

        Note: This will find all complete melds, even if some cards are used
        in more than one.
        """
        if self._detected is False:
            self._find_runs()
            self._find_sets()
            self._detected = True

    def _find_runs(self):
        """Find all runs in the hand and create melds for them.

        Note: *all* runs are found, even those that are subsets of other runs. If the
        3, 4, 5, and 6 of hearts are in the hand, three runs will be found - (3,4,5),
        (4,5,6), and (3,4,5,6).
        """

        def group_by_suit(input_list):
            # generator that yields a list of cards in each suit represented
            #  in input_list
            #
            # (assumes input list is already sorted)
            by_suit = groupby(
                input_list,
                key=lambda card: card.suit
            )
            for suit, suit_group in by_suit:
                yield list(suit_group)

        def get_all_sequences(input_list): #!FIXME - move to CardStack?
            # generator that yields a tuple for each card sequences in the input list
            #  wherein each card is consecutively sequenced by card ranks
            temp_list = cycle(input_list)
            next(temp_list)
            groups = groupby(
                input_list,
                key=lambda j: j.rank.value+1 == next(temp_list).rank.value
            )
            for k, v in groups:
                if k:
                    yield tuple(v) + (next((next(groups)[1])), )

        def all_runs_in_sequences(sequences): #!FIXME - move to CardStack?
            # generator that yields a tuple for every run (sequence w/ len>=3)
            #  in the input list of sequences
            #
            # e.g. input 2,3,4,5 yields (2,3,4),(3,4,5),(2,3,4,5)
            for seq in sequences:
                print("seq is {}".format(seq))
                for seq_len in range(3, len(seq)+1): # will be null if len<3
                    print("seq_len is {}".format(seq_len))
                    yield zip(*(seq[i:] for i in range(seq_len)))

        self._sort_cards()
        print("going into run detection, cards: {}".format(self._cards))
        runs = [
            run
            for suit_group in group_by_suit(self._cards)
            for sublist in all_runs_in_sequences(get_all_sequences(suit_group))
            for run in sublist
        ]

        for run in runs:
            self.create_meld(*list(run))

    def _find_sets(self):
        """Find all sets in the hand and create melds for them.

        Note: *all* sets are found, even those that are subsets of other sets.
        """
        #!FIXME - implement

    @property
    def is_complete_hand(self) -> bool:
        """True if there are 10 or 11 cards in the hand."""
        return len(self.cards) == 10 or len(self.cards) == 11

    def detect_optimal_melds(self) -> None:
        """Find the best set of melds in the hand."""
        self._detect_all_melds()
        overused = self.get_melds_with_overused_cards()

        # completion conditions, easiest-to-detect first
        if self.deadwood_count > 1:
            # not winning
            return

        if len(overused) == 0 and self.deadwood_count == 0:
            # winning hand
            return

        if len(overused) == 0 and self.deadwood_count == 1:
            # winning, with some deadwood
            return

        # now things get tricky - if there is no deadwood *but* there are some
        # overused cards then we need to see if there is a set of melds that avoids
        # card overuse without deadwood
        #!FIXME - implement
