"""Controller for game of gin rummy."""

from pylgrum.player import Player
from pylgrum import Deck, Card, CardStack

class Game():

    def __init__(self, p1: Player, p2: Player) -> None:
        self.p1 = p1
        self.p2 = p2

        self._deck = Deck()
        self._deck.shuffle()

        self._discards = CardStack()

        for x in range(0, 10):
            self.p1.receive_card(self._deck.draw())
            self.p2.receive_card(self._deck.draw())

        self._discards.add(self._deck.draw())

        self._next_player = self.p1
        self._num_moves = 0

    def draw(self) -> Card:
        """Called by a Player to draw from the deck."""
        return self._deck.draw()

    def draw_discard(self) -> Card:
        """Called by a Player to take the visible discarded card."""
        return self._discards.draw()

    def _alternate_player(self) -> None:
        """Switch between p1 and p2."""
        if self._next_player == self.p1:
            self._next_player = self.p1
        elif self._next_player == self.p2:
            self._next_player = self.p2
        else:
            print("TOTALLY IMPOSSIBLE - INTERNAL ERROR")

    def play(self) -> None:
        """Play a game by alternating moves until one player knocks."""
        while True:
            (discard, did_knock) = self._next_player.play(self._discards.peek())
            if did_knock is True:
                # FIXME: validate meld legitimacy
                # FIXME: check for super-gin
                # FIXME: deal with deadwood in non-gin knock scenario
                if self._next_player == self.p1:
                    winner = "Player 1"
                else:
                    winner = "Player 2"
                print("{} wins".format(winner))
                break
            self._discards.add(discard)
            self._alternate_player()
