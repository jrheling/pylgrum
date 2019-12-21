"""Controller for game of gin rummy."""

from pylgrum.player import Player
from pylgrum.move import Move, CardSource, MoveState
from pylgrum import Deck, Card, CardStack

class Game():
    """Base class for a game of gin rummy."""

    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

        self._deck = Deck()
        self._deck.shuffle()

        self._discards = CardStack()

        for _ in range(0, 10):
            self.player1.receive_card(self._deck.draw())
            self.player2.receive_card(self._deck.draw())

        self._discards.add(self._deck.draw())

        self._current_player = self.player1
        self._current_move = None
        self._num_moves = 0

        self._knocked = False

    def _draw(self) -> Card:
        """Draw from the deck."""
        return self._deck.draw()

    def _draw_discard(self) -> Card:
        """Take the visible discarded card."""
        return self._discards.draw()

    def _alternate_player(self) -> None:
        """Called between moves.

        Side effects:
         * switches _current_player pointer
         * increment move counter
        """
        self._num_moves += 1

        if self._current_player == self.player1:
            self._current_player = self.player2
        elif self._current_player == self.player2:
            self._current_player = self.player1
        else:
            print("TOTALLY IMPOSSIBLE - INTERNAL ERROR") #FIXME raise instead

    def pre_turn_hook(self):
        """Called before each move. For sub-class use."""
        pass

    def post_turn_hook(self):
        """Called after each move. For sub-class use."""
        pass

    def _do_turn(self):
        """Interact with a Player to make a Move.

        Side effects:
         * gives player card via the acquired property of the Move
         * calls pre_turn_hook and post_turn_hook
        """
        self.pre_turn_hook()
        self._current_move = Move(self._discards.peek())
        self._current_player.turn_start(self._current_move)
        if self._current_move.card_source == CardSource.DRAW_STACK:
            self._current_move.acquired = self._draw()
        elif self._current_move.card_source == CardSource.DISCARD_STACK:
            self._current_move.acquired = self._draw_discard()

        self._current_player.turn_finish(self._current_move)

        if self._current_move.knocking is True:
            #### game is ending
            # FIXME: validate meld legitimacy
            # FIXME: check for super-gin
            # FIXME: deal with deadwood in non-gin knock scenario
            self._knocked = True
            print("{} wins".format(self._current_player))
            return

        assert self._current_move.state == MoveState.COMPLETE
        self._discards.add(self._current_move.discarded)
        self.post_turn_hook()

    def play(self) -> None:
        """Play a game by alternating moves until one player knocks."""
        while True:
            self._current_move = Move(self._discards.peek())
            self._do_turn()
            if self._current_move.knocking is True:
                print("{} has knocked to end the game".
                      format(self._current_player))
                # FIXME - add validity checking & scoring
                break
            self._alternate_player()
