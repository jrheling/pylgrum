"""Hand subclass that finds the best melds in a set of cards."""

from itertools import cycle, groupby, combinations

from pylgrum.hand import Hand
from pylgrum.card import Card, Suit, Rank
from pylgrum.hand_melds import HandWithMelds
from pylgrum.errors import InvalidHand

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
        self.optimal_hand = HandWithMelds()
        if cards:
            self.add(cards)
            self.optimal_hand.add(cards)

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

        def all_runs_in_sequences(sequences):
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
            for suit_group in self.group_by_suit()
            for sublist in all_runs_in_sequences(MeldDetector.get_all_sequences(suit_group))
            for run in sublist
        ]

        for run in runs:
            self.create_meld(*list(run))

    def _find_sets(self):
        """Find all sets in the hand and create melds for them.

        Note: *all* sets are found, even those that are subsets of other sets.
        """
        sorted_by_rank = sorted(self._cards, key=lambda card: card.rank.value)
        grouped_by_rank = groupby(sorted_by_rank, key=lambda card: card.rank)

        for _, cards_of_rank_X in grouped_by_rank:
            cards = list(cards_of_rank_X)
            if len(cards) == 4:
                # 4 distinct 3-long sets, 1 4-long set
                for combo in combinations(cards, 3):
                    self.create_meld(*combo)
                self.create_meld(*cards)
                pass
            elif len(cards) == 3:
                self.create_meld(*cards)

    @property
    def is_complete_hand(self) -> bool:
        """True if there are 10 or 11 cards in the hand."""
        return len(self.cards) == 10 or len(self.cards) == 11

    def detect_optimal_melds(self) -> None:
        """Find the best set of melds in the hand."""
        self._detect_all_melds()
        overused = self.melds_with_overused_cards()

        # if no cards are in multiple melds, then "optimal" is easy
        if len(overused) == 0:
            for meld in self._melds:
                self.optimal_hand.create_meld(*meld.cards)
        else:
            """
            A complete hand can only use each card once (no "overuse"), but
            if we got here it means the set of all potential melds includes
            some that overuse at least some cards.

            By definition, the "optimal" set of melds is that which leaves
            the smallest deadwood (by point value).

            This algorithm brute-forces its way to discovering the optimal set.

            1) build a list of potential hands (sets of melds) that don't overuse
             - each card used in N (N>1) sets represents N possible hands
             - for each meld the card is in:
                - create a potential hand that only uses that card in that one meld
            """ #! FIXME - correct the docs to match reality

            possible_hands = []
            # find each meld that contains overused card
            for meld_to_resolve in self.melds_with_overused_cards(complete=True):
                cards_to_resolve = list(filter(
                    lambda card: len(self.melds_using_card(card)) > 1,
                    meld_to_resolve.cards
                ))
                if len(cards_to_resolve) > 1:
                    # !starting simple, with only a single overused card per meld
                    print("skipping over meld with >1 overused cards")
                    continue
                    # raise NotImplementedError
                for card in cards_to_resolve:
                    # try a hand in which this card is only used in this meld
                    possible_hand = HandWithMelds()
                    possible_hand.add(self.cards)

                    # first put all complete melds into our possible hand
                    for meld in filter(
                        lambda m: m.complete,
                        self.melds
                    ):
                        possible_hand.create_meld(*meld.cards)

                    # now remove the current card from the N-1 of the melds that use it
                    meld_being_resolved = next(filter(
                        lambda meld: meld == meld_to_resolve,
                        possible_hand.melds_using_card(card)
                    ))
                    melds_losing_this_card = filter(
                        lambda meld: meld != meld_to_resolve,
                        possible_hand.melds_using_card(card)
                    )
                    for meld in melds_losing_this_card:
                        meld.remove(meld.find(card))
                        # removing this card may have made the meld incomplete
                        #  - if so, remove it
                        # Note: this is gratuitious, b/c incomplete melds will
                        #  just be ingored later
                        if not meld.complete:
                            possible_hand.remove_meld(meld)

                    possible_hands.append(possible_hand)

            best_hand = None
            for hand_being_evaluated in possible_hands:
                try:
                    score = hand_being_evaluated.deadwood_value
                except InvalidHand:
                    print("skipping invalid hand")
                    next
                if best_hand is None:
                    best_hand = hand_being_evaluated
                elif hand_being_evaluated.deadwood_value < best_hand.deadwood_value:
                    best_hand = hand_being_evaluated

            self.optimal_hand = best_hand

            # raise NotImplementedError

        #!FIXME - implement
