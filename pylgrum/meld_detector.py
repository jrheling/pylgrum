"""Hand subclass that finds the best melds in a set of cards."""

from itertools import groupby, combinations, permutations

from pylgrum.card import Card
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

    @property
    def is_complete_hand(self) -> bool:
        """True if there are 10 or 11 cards in the hand."""
        return len(self.cards) == 10 or len(self.cards) == 11

    # These do not make sense for HandDetector instances, and will not behave
    # in a useful, reliable, or helpful way. Make that clear by raising
    def remove(self, i: int):
        # no use case for this yet, but if needed it could be implemented as a
        #  combination of super().find() and super().remove()
        raise NotImplementedError

    def get(self, i: int):
        raise NotImplementedError

    def find(self, targetcard: Card):       # parent method returns an index
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def peek(self):        # "top" of stack is meaningless here
        raise NotImplementedError

    # The following methods all simply wrap their superclass implementations for
    #  the purpose of unsetting our _detected flag.
    def add(self, newcard: Card) -> None:
        """Extends base method to add a card to the hand."""
        super().add(newcard)
        self._sort_cards()

    def detect_optimal_melds(self) -> None:
        """Find the best set of melds in the hand."""
        self._detect_all_melds()
        overused = self.melds_with_overused_cards(complete=True)
        # print("** non-overused melds: {}".format(
        #   self.melds_with_no_overused_cards(complete=True)
        # ))
        # print("** overused melds: {}\n".format(
        #   self.melds_with_overused_cards(complete=True)
        # ))

        # if no cards are in multiple melds, then "optimal" is easy
        if len(overused) == 0:
            for meld in self._melds:
                self.optimal_hand.create_meld(*meld.cards)
        else:
            #
            # A complete hand can only use each card once (no "overuse"), but
            # if we got here it means the set of all potential melds includes
            # some that overuse at least some cards.
            #
            # By definition, the "optimal" set of melds is that which leaves
            # the smallest deadwood (by point value).
            #
            # This algorithm brute-forces its way to discovering the optimal set.
            #

            # might IMPROVEME by making a set (need to define __hash__  on HandWithMelds)
            possible_hands = []
            melds_with_overuse = self.melds_with_overused_cards(complete=True)
            # Compute every possible ordering of them. A winning hand can never
            #  use more than 3 melds, so we can look just at that length.
            meld_orderings = permutations(melds_with_overuse, min(3, len(melds_with_overuse)))
            for ordering in meld_orderings:
                possible_hands.append(self._solve_hand_for_melds_in_order(ordering))

            best_hand = None
            for hand_being_evaluated in possible_hands:
                try:
                    if best_hand is None:
                        # hack so we raise before setting best_hand
                        assert hand_being_evaluated.deadwood_value

                        best_hand = hand_being_evaluated
                        # print("initializing best_hand: {}".format(best_hand.melds))
                    elif hand_being_evaluated.deadwood_value < best_hand.deadwood_value:
                        best_hand = hand_being_evaluated
                        # print("new best hand: {}".format(best_hand.melds))
                except InvalidHand:
                    # print("skipping invalid hand: {}".format(hand_being_evaluated.melds))
                    continue

            # print("FINAL best hand: {} (deadwood={})".format(
            #     best_hand.melds, best_hand.deadwood_value
            # ))
            self.optimal_hand = best_hand

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
            self._find_complete_sets()
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
                # print("seq is {}".format(seq))
                for seq_len in range(3, len(seq)+1): # will be null if len<3
                    # print("seq_len is {}".format(seq_len))
                    yield zip(*(seq[i:] for i in range(seq_len)))

        self._sort_cards()
        # print("going into run detection, cards: {}".format(self._cards))
        runs = [
            run
            for suit_group in self.group_by_suit()
            for sublist in all_runs_in_sequences(MeldDetector.get_all_sequences(suit_group))
            for run in sublist
        ]

        for run in runs:
            self.create_meld(*list(run))

    def _find_complete_sets(self):
        """Find all complete sets in the hand and create melds for them.

        Note: *all* sets are found, even those that are subsets of other sets.
        """
        sorted_by_rank = sorted(self._cards, key=lambda card: card.rank.value)
        grouped_by_rank = groupby(sorted_by_rank, key=lambda card: card.rank)

        for _, cards_of_rank_x in grouped_by_rank:
            cards = list(cards_of_rank_x)
            if len(cards) == 4:
                # 4 distinct 3-long sets, 1 4-long set
                for combo in combinations(cards, 3):
                    self.create_meld(*combo)
                self.create_meld(*cards)
            elif len(cards) == 3:
                self.create_meld(*cards)

    def _solve_hand_for_melds_in_order(self, ordering) -> HandWithMelds:
        """Return the possible hand created by resolving meld conflicts
        in the specified order."""

        # Notation: in this context, "solving" a meld means making
        #  it no longer a card-overusing meld (by removing the cards
        #  in this meld from other melds).

        # init the new hand in which we'll describe this possible solution
        possible_hand = HandWithMelds()
        possible_hand.add(self.cards)
        for meld in filter(lambda m: m.complete, self.melds):
            possible_hand.create_meld(*meld.cards)

        for meld_to_solve in ordering:
            # earlier meld resolution could have either removed this meld
            #  b/c it became invalid or solved it - in either case we've
            #  nothing more to do
            if meld_to_solve not in possible_hand.melds:
                continue
            if meld_to_solve not in possible_hand.melds_with_overused_cards(complete=True):
                continue

            # print('=' * 50)
            # print("resolving overused meld {}".format(meld_to_solve))
            cards_to_solve = list(filter(
                lambda card: len(possible_hand.melds_using_card(card)) > 1,
                meld_to_solve.cards
            ))

            for card in cards_to_solve:
                # remove the current card from all other melds

                # print(". resolving card {}".format(card))
                # print("  hand: {}".format(possible_hand.melds))

                melds_losing_this_card = filter(
                    # pylint: disable=cell-var-from-loop
                    lambda meld: meld != meld_to_solve,
                    # pylint: enable=cell-var-from-loop
                    possible_hand.melds_using_card(card)
                )

                for meld in melds_losing_this_card:
                    # print(" . removing {} from meld {} in potential new hand".format(card, meld))
                    possible_hand.remove_from_meld(meld, card)

                    if not meld.complete:
                        # print("  .. that made meld incomplete - removing it")
                        possible_hand.remove_meld(meld)
                # print("  hand now: {}".format(possible_hand.melds))

        # print("resolution of {} yielded hand: {}".format(meld_to_solve, possible_hand.melds))
        return possible_hand
