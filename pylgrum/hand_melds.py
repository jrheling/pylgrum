"""Hand subclass that allows the user to arrange cards by potential meld."""

from pylgrum import Hand, CardStack, Card, InvalidMeldError, Meld

class HandWithMelds(Hand):
    """Builds on Hand to track partial/complete melds within a hand.

    This class lets a user sort the cards in the hand into melds and potential
    melds. For human users this facilitates display of the hand during game
    play. Machine users could further subclass HandWithMelds to support
    reasoning about mvoe strategy."""

    def __init__(self) -> None:
        super().__init__()
        self._melds = []     # list of Melds - NOTE - do not add cards to
                             #   these melds directly - *only* use the
                             #   below methods (in order to keep the
                             #   _card_to_meld_id map correct)
        self._card_to_meld_id = {}    # map card to set of Melds it belongs to
        self._meld_id_to_meld = {}
        
    @property
    def melds(self) -> list:
        return self._melds
        
    def create_meld(self, *cards) -> None:
        """Create a new [potential] meld within the hand.

        Optionally, initial cards for the meld may be supplied. If they are, 
        they must be valid - an attempt to create an invalid meld on init
        will cause the whole thing to be deleted.

        Raises InvalidMeldError.
        """
        # note: no check against redundant melds
        new_meld = Meld()
        added = []
        valid = True
        for card in cards:
            try:
                self.add_to_meld(new_meld, card)
            except InvalidMeldError:
                valid = False
            else:
                added.append(card)
        if not valid:
            for card in added:
                self.remove_from_meld(new_meld, card)
            raise InvalidMeldError("non-meld passed "
                                   + "to HandWithMeld:create_meld()")
        else:
            self._melds.append(new_meld)
            self._meld_id_to_meld[id(new_meld)] = new_meld

    def remove_meld(self, meld: Meld) -> None:
        """Remove a meld.

        Removes references to the meld from _card_to_meld_id mapping.
        """
        for card in meld.cards:
            self.remove_from_meld(meld, card)
        self._melds.remove(meld)

    def add_to_meld(self, meld: Meld, card: Card) -> None:
        """Add a card to a meld.

        Args:
         * meld: the meld to add to
         * card: the card to add

        Side effects:
         * Updates _card_to_meld_id map accordingly
        
        Raises InvalidMeldError.
        """
        meld.add(card)
        if card in self._card_to_meld_id.keys():
            self._card_to_meld_id[card].add(id(meld))
        else:
            self._card_to_meld_id[card] = set([id(meld)])

    def remove_from_meld(self, meld: Meld, card: Card) -> None:
        """Remove a card from a meld

        Args:
         * meld: the meld to add to
         * card: the card to add

        Side effects:
         * Updates _card_to_meld_id map accordingly
         * Removes entry from _card_to_meld_id if empty
        """
        self._card_to_meld_id[card].remove(id(meld))
        if len(self._card_to_meld_id[card]) == 0:
            del self._card_to_meld_id[card]
        meld.remove(meld.find(card))
            
    def add_to_meld_by_idx(self, meld_idx: int, card_idx: int) -> None:
        """Wrapper on add_to_meld; works with indices rather than objects."""
        if meld_idx not in range(0,len(self._melds)):
            print("DB: idx = {}, len == {}".format(meld_idx, len(self._melds)))
            raise InvalidMeldError("No meld at index position {}".
                                   format(meld_idx))
        if card_idx not in range(0,self.size()):
            raise InvalidMeldError("No card at index position {}".
                                   format(card_idx))
        return self.add_to_meld(
            self._melds[meld_idx],
            self.cards[card_idx]
        )

    def melds_using_card(self, card: Card) -> list:
        """Returns list of Melds that use the given Card (or None)."""
        if card in self._card_to_meld_id.keys():
            return [self._meld_id_to_meld[x]
                    for x in self._card_to_meld_id[card]]
        else:
            return None
    
    # note: need to deal with assessing validity given the possiblity of
    #  mutually incompatible melds (i.e. those that use the same card)
