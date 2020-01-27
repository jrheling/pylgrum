"""Text UI (TUI) implementation of Gin Rummy player."""

from pylgrum.card import Card
from pylgrum.hand import Hand
from pylgrum.move import Move
from pylgrum.player import Player
from pylgrum.tui.hand_melds import HandWithMelds
from pylgrum.errors import InvalidMeldError

from pylgrum.tui.util import clear_screen

class TUIPlayer(Player):
    """Terminal-based interface for a human Gin Rummy player."""

    def __init__(self, player_id: str):
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
        """See available discard, choose where to get card."""
        self.print_turn_screen()
        # self.clear_screen()
        # self.print_banner(self.banner_text)
        # self.show_hand()
        #print("\nAvailable discard: {}".format(move.available_discard))
        self.action_text("Take discard or draw?")
        print()
        self.context("Available discard: {}".
                     format(move.available_discard))
        print()
        new_card_from = None
        while new_card_from not in ["1","2"]:
            # print("dbug: new_card_from is {} (type {})".
            #       format(new_card_from,
            #              type(new_card_from)))
            new_card_from = self._prompt_card_from()

        if new_card_from == "1":
            print("... taking discard into hand")
            move.choose_card_from_discard()
        elif new_card_from == "2":
            print("... taking card from draw pile")
            move.choose_card_from_draw()

    def turn_finish(self, move: Move) -> Move:
        """See acquired card, choose discard."""
        super().turn_finish(move) # need to call to put new card in hand
        print("Current hand:\n")
        self.show_hand()
        self.manage_hand()
        if self.knocking:
            move.knocking = True
        # FIXME: allow super-gin by making post-knock discard optional
        discard = None
        while discard not in range(1,12):
            #print("DB: discard = {}".format(discard))
            discard = self._prompt_discard()

        move.discard(self.hand.get(discard - 1))

    def meld_references(self, card: Card) -> str:
        """Returns a string characterizing the melds in which a Card is used.

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
        melds = self._hand.melds_using_card(card)
        if melds is None:
            return ""
        else:
            complete_s = 0
            complete_r = 0
            partial_s = 0
            partial_r = 0
            partial_other = 0
            for m in melds:
                if m.is_set:
                    complete_s += 1
                elif m.is_run:
                    complete_r += 1
                elif m.all_same_suit and m.all_same_rank:
                    partial_other += 1
                elif m.all_same_suit:
                    partial_r += 1
                elif m.all_same_rank:
                    partial_s += 1
            return("[{}".format('S' * complete_s)
                   + "{}".format('R' * complete_r)
                   + "{}".format('s' * partial_s)
                   + "{}".format('r' * partial_r)
                   + "{}]".format('?' * partial_other))


    def show_hand(self):
        """Displays the current hand."""
        for (index, card) in enumerate(self._hand.cards):
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
        if len(self._hand.melds) == 0:
            print("No melds defined.")

        for i in range(1, len(self._hand.melds)+1):
            meld = self._hand.melds[i-1]
            if meld.complete:
                status = " "
                if meld.is_run:
                    type = "run"
                elif meld.is_set:
                    type = "set"
            else:
                status = "?"
                if meld.all_same_suit and meld.all_same_rank:
                    type = "???"
                elif meld.all_same_suit:
                    type = "run"
                elif meld.all_same_rank:
                    type = "set"

            if meld.size() == 0:
                type = "null"
                status = ""

            print("#{idx}:{type}{status}: {cards}".format(
                idx=i,
                type=type,
                status=status,
                cards=[str(x) for x in meld.cards]
            ))

    @staticmethod
    def print_banner(heading: str,
                     width: int = 80,
                     sep_char: str = '=') -> None:
        """Prints a banner with centered text and heading/footing rows.

        Arguments:
         * heading - the string to print
         * width - the size of the space in which to center the heading
         * sep_char - single char repeated as necessary to fill the width
                         of the heading / footing rows
        """
        print("{t:{s}^{w}}".format(t='', s='=', w=80))
        print("{t:^{w}}".format(t=heading, s=sep_char, w=width))
        print("{t:{s}^{w}}".format(t='', s=sep_char, w=width))

    @staticmethod
    def print_subheading(heading: str,
                         width: int = 80,
                         sep_char: str = '-') -> None:
        """Prints text centered on a single line filled with specified char."""
        if len(heading):
            heading = " {} ".format(heading)
        print("  {t:{s}^{w}}  ".format(t = heading,
                                       s = sep_char,
                                       w = width - 4))

    @staticmethod
    def action_text(text: str,
                    width: int = 80,
                    prefix: str = "==>",
                    suffix: str = "<==") -> None:
        """Prints text, centered with attention-getting prefix & suffix."""
        line = "{} {} {}".format(prefix, text, suffix)
        print("{t:^{w}}".format(t=line, w=width))

    @staticmethod
    def context(text: str,
                prefix: str = "%%%") -> None:
        """Prints specified text with attention-getting prefix."""
        if len(prefix):
            prefix = " {} ".format(prefix)
        print("{}{}".format(prefix, text))

    @staticmethod
    def normalize_input(c):
        """Return int version of number chars.

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
            r = int(c)
        except ValueError:
            # get here if c was a string
            r = c

        return r

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
            if command in ("c","C"):
                self._hand.create_meld()
                print("(created new meld)")
            elif command in ("a","A"):
                #self.show_melds()
                m = None
                while m not in ('n','N',*range(1,len(self._hand.melds)+1)):
                    m = self.normalize_input(input(
                        "Enter the number of the meld to "
                        + "add to, or 'N' for a new meld: "))
                    if m in ('n','N'):
                        self._hand.create_meld()
                        m = len(self._hand.melds) # len() is 1-indexed
                        break ## loop stopping condition was computed
                              ##  before we added to the meld list
                    # print("debug: end of while m loop m=={} ({})".
                    #       format(m, type(m)))
                # it should only be possible to get here with m set to
                #  one more than the index of the target meld
                c = None
                while c not in ('x','X'):
                    c = self.normalize_input(input(
                        "card to add? (x when finished) "))
                    if c in range(1,12):
                        try:
                            self._hand.add_to_meld_by_idx(m - 1, c - 1)
                        except InvalidMeldError:
                            print("Can't add {} ".
                                  format(self._hand.cards[c-1])
                                  + " to meld {}".
                                  format(self._hand.melds[m-1]))
                        else:
                            print("Added {} ".format(self._hand.cards[c-1])
                                  + "to meld {}.".format(
                                    self._hand.melds[m-1])
                            )
            elif command in ("r","R"):
                #self.show_melds()
                m = None
                while m not in range(1,len(self._hand.melds)+1):
                    m = self.normalize_input(input(
                        "Enter the number of the meld to remove: "))
                self._hand.remove_meld(self._hand.melds[m-1])
            elif command in ("d","D"):
                break
            elif command in ("k","K"):
                # FIXME: add check to make sure knock will be legal
                self.knocking = True
                break
            else:
                # invalid command
                next
