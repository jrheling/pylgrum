"""Text-mode player subclass, implements very basic console UI."""

from pylgrum.card import Card
from pylgrum.move import Move
from pylgrum.player import Player
from pylgrum.tui.hand_melds import HandWithMelds
from pylgrum.errors import InvalidMeldError

from pylgrum.tui.util import clear_screen

class TUIPlayer(Player):
    """Terminal-based interface for a human Gin Rummy player."""

    def __init__(self, player_id: str):
        """Create and initialize a player.

        Args:
            player_id (str): display name for the player
        """
        self._player_id = player_id
        """Used to identify the player in the UI."""

        super().__init__(handtype=HandWithMelds)
        self.knocking = False
        self.banner_text = "{}'s turn".format(self.__str__())

    def __str__(self):
        return self._player_id

    @staticmethod
    def _prompt_card_from() -> str:
        return input("Press 1 to take the discard, 2 to draw: ")

    @staticmethod
    def _prompt_discard() -> str:
        return TUIPlayer.normalize_input(input(
            "Enter the number of the card you want to discard: "))

    def turn_start(self, move: Move) -> Move:
        """Show available discard, choose where to get card.

        Args:
            move (Move): the move object used for this turn

        This implements the abstract base method (hook).
        """
        self.print_turn_screen()
        self.action_text("Take discard or draw?")
        print()
        self.context("Available discard: {}".
                     format(move.available_discard))
        print()
        new_card_from = None
        while new_card_from not in ["1", "2"]:
            new_card_from = self._prompt_card_from()

        if new_card_from == "1":
            print("... taking discard into hand")
            move.choose_card_from_discard()
        elif new_card_from == "2":
            print("... taking card from draw pile")
            move.choose_card_from_draw()

    def turn_finish(self, move: Move) -> Move:
        """Show acquired card, choose card to discard.

        Args:
            move (Move): the move object used for this turn

        This implements the abstract base method (hook).
        """
        super().turn_finish(move) # need to call to put new card in hand
        print("Current hand:\n")
        self.show_hand()
        self.manage_hand()
        if self.knocking:
            move.knocking = True
        # FIXME: allow super-gin by making post-knock discard optional
        discard = None
        while discard not in range(1, 12):
            #print("DB: discard = {}".format(discard))
            discard = self._prompt_discard()

        move.discard(self.hand.get(discard - 1))

    def meld_references(self, card: Card) -> str:
        """Returns a string characterizing the melds in which a Card is used.

        Args:
            card (Card): the card whose references are sought

        The string uses a single character for each meld the card is part
        of. That string will be:

         'S' : complete set
         'R' : complete run
         's' : partial set
         'r' : partial run
         '?' : other partial

        All complete melds will be referenced first.

        If the card is referenced in no melds, an empty string is returned.
        If a non-empty string is returned, it is wrapped in square brackets.
        """
        melds = self.hand.melds_using_card(card)
        if melds is not None:
            complete_s = 0
            complete_r = 0
            partial_s = 0
            partial_r = 0
            partial_other = 0
            for meld in melds:
                if meld.is_set:
                    complete_s += 1
                elif meld.is_run:
                    complete_r += 1
                elif meld.all_same_suit and meld.all_same_rank:
                    partial_other += 1
                elif meld.all_same_suit:
                    partial_r += 1
                elif meld.all_same_rank:
                    partial_s += 1
            return("[{}".format('S' * complete_s)
                   + "{}".format('R' * complete_r)
                   + "{}".format('s' * partial_s)
                   + "{}".format('r' * partial_r)
                   + "{}]".format('?' * partial_other))
        return ""

    def show_hand(self):
        """Display the current hand."""
        for (index, card) in enumerate(self.hand.cards):
            print("{}: {} {}".format(
                index+1,
                card,
                self.meld_references(card)
            ))

    def show_melds(self) -> None:
        """Display current melds so user can manage their hand.

        Lists every potential or actual meld and its contents, and
        shows user which cards are being used in multiple melds (these
        cards represent choices they'll have to make).
        """
        if len(self.hand.melds) == 0:
            print("No melds defined.")

        for i in range(1, len(self.hand.melds)+1):
            meld = self.hand.melds[i-1]
            if meld.complete:
                status = " "
                if meld.is_run:
                    meld_type = "run"
                elif meld.is_set:
                    meld_type = "set"
            else:
                status = "?"
                if meld.all_same_suit and meld.all_same_rank:
                    meld_type = "???"
                elif meld.all_same_suit:
                    meld_type = "run"
                elif meld.all_same_rank:
                    meld_type = "set"

            if meld.size() == 0:
                meld_type = "null"
                status = ""

            print("#{idx}:{meld_type}{status}: {cards}".format(
                idx=i,
                meld_type=meld_type,
                status=status,
                cards=[str(x) for x in meld.cards]
            ))

    @staticmethod
    def print_banner(heading: str,
                     width: int = 80,
                     sep_char: str = '=') -> None:
        """Print a banner with centered text and heading/footing rows.

        Arguments:
            heading (str): the string to print
            width (int): the size of the space in which to center the heading
            sep_char (str): single char repeated as necessary to fill the width
                            of the heading / footing rows
        """
        print("{t:{s}^{w}}".format(t='', s='=', w=80))
        print("{t:^{w}}".format(t=heading, w=width))
        print("{t:{s}^{w}}".format(t='', s=sep_char, w=width))

    @staticmethod
    def print_subheading(heading: str,
                         width: int = 80,
                         sep_char: str = '-') -> None:
        """Print text centered on a single line filled with specified char."""
        if len(heading) > 0:
            heading = " {} ".format(heading)
        print("  {t:{s}^{w}}  ".format(t=heading,
                                       s=sep_char,
                                       w=width - 4))

    @staticmethod
    def action_text(text: str,
                    width: int = 80,
                    prefix: str = "==>",
                    suffix: str = "<==") -> None:
        """Print text, centered with attention-getting prefix & suffix."""
        line = "{} {} {}".format(prefix, text, suffix)
        print("{t:^{w}}".format(t=line, w=width))

    @staticmethod
    def context(text: str,
                prefix: str = "%%%") -> None:
        """Print specified text with attention-getting prefix."""
        if len(prefix) > 0:
            prefix = " {} ".format(prefix)
        print("{}{}".format(prefix, text))

    @staticmethod
    def normalize_input(input_char):
        """Return int version of number chars.

        Args:
            input_char (str): a single character

        This is used to simplify input checking that uses range(). It takes
        a character and returns the int equivalent for number characters,
        and returns the input unchanged for non-number characters.

        For example:
        normalize_input('c') -> 'c'   # str
        normalize_input('1') -> 1     # int
        normalize_input('D') -> 'D'   # str
        normalize_input('42') -> 42   # int
        """
        try:
            r_val = int(input_char)
        except ValueError:
            # get here if c was a string
            r_val = input_char

        return r_val

    def print_turn_screen(self) -> None:
        """Clear screen, show hand, show melds."""
        clear_screen()
        self.print_banner(self.banner_text)
        self.print_subheading("current hand")
        self.show_hand()
        print("\n",)
        self.print_subheading("current melds")
        self.show_melds()
        print("\n",)
        self.print_subheading("available action")

    #pylint: disable=too-many-branches
    def manage_hand(self) -> None:
        """Show hand, let user arrange (potential) melds.

        Loops until user chooses to discard.
        """
        ## NOTE: user-facing views index from 1, not 0

        while True:
            self.print_turn_screen()
            self.action_text("Update melds as desired, then choose a discard.")
            print()
            self.context("Manage hand: [A]dd card to meld, [R]emove meld")
            self.context("Finish turn: [D]iscard, [K]nock (end game)")
            print()
            #print(manage_prompt)

            command = input("> ")
            if command in ("c", "C"):
                self.hand.create_meld()
                print("(created new meld)")
            elif command in ("a", "A"):
                #self.show_melds()
                meld_num = None
                while meld_num not in ('n', 'N', *range(1, len(self.hand.melds)+1)):
                    meld_num = self.normalize_input(input(
                        "Enter the number of the meld to "
                        + "add to, or 'N' for a new meld: "))
                    if meld_num in ('n', 'N'):
                        self.hand.create_meld()
                        meld_num = len(self.hand.melds) # len() is 1-indexed
                        break ## loop stopping condition was computed
                              ##  before we added to the meld list
                    # print("debug: end of while m loop m=={} ({})".
                    #       format(m, type(m)))
                # it should only be possible to get here with m set to
                #  one more than the index of the target meld
                card_num = None
                while card_num not in ('x', 'X'):
                    card_num = self.normalize_input(input(
                        "card to add? (x when finished) "))
                    if card_num in range(1, 12):
                        try:
                            self.hand.add_to_meld_by_idx(meld_num - 1, card_num - 1)
                        except InvalidMeldError:
                            print("Can't add {} ".
                                  format(self.hand.cards[card_num-1])
                                  + " to meld {}".
                                  format(self.hand.melds[meld_num-1]))
                        else:
                            print("Added {} ".format(self.hand.cards[card_num-1])
                                  + "to meld {}.".format(
                                      self.hand.melds[meld_num-1]
                                  ))
            elif command in ("r", "R"):
                meld_num = None
                while meld_num not in range(1, len(self.hand.melds)+1):
                    meld_num = self.normalize_input(input(
                        "Enter the number of the meld to remove: "))
                self.hand.remove_meld(self.hand.melds[meld_num-1])
            elif command in ("d", "D"):
                break
            elif command in ("k", "K"):
                # FIXME: add check to make sure knock will be legal
                self.knocking = True
                break
            #else invalid command
