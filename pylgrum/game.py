"""Controller for game of gin rummy."""

from pylgrum.player import Player
from pylgrum.move import Move, CardSource, MoveState
from pylgrum import Deck, Card, CardStack, IllegalMoveError, PylgrumInternalError, CardNotFoundError

class Game():
    """Base class for a game of gin rummy."""

    def __init__(self, player1: Player, player2: Player, game_id: str = None) -> None:
        self.player1 = player1
        self.player2 = player2

        self.game_id = game_id

        self.player1.join_game(self)
        self.player2.join_game(self)

        self._deck = Deck()
        self._deck.shuffle()

        self._discards = CardStack()

        for _ in range(0, 10):
            self.player1.receive_card(self._deck.draw())
            self.player2.receive_card(self._deck.draw())

        self._discards.add(self._deck.draw())

        self._current_player = self.player1
        self.current_move = None
        self._num_moves = 0

        self._knocked = False

    @property
    def current_player(self):
        return self._current_player

    @property
    def visible_discard(self):
        return self._discards.peek()

    @property
    def contestant_ids(self):
        return [ p.contestant_id for p in [self.player1, self.player2]]

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

    def start_new_move(self):
        """Called at the start of a turn.

        If called while a move is in progress, raises IllegalMoveError.

        Is a no-op if called when the current_move is already in the "new" state.
        """
        if self.current_move is not None:
            if self.current_move.state == MoveState.IN_PROGRESS:
                raise IllegalMoveError("start_new_move() called while move was in progress")
            if self.current_move.state == MoveState.NEW:
                # no-op
                return
        self.current_move = Move(self._discards.peek())

    def acquire_card(self) -> None:
        """Add card from the selected source to the hand.

        Card source is configured in the Move - calling this before that has
        been done will raise IllegalMoveError.
        """
        if (self.current_move.state != MoveState.IN_PROGRESS):
            raise IllegalMoveError("Got to _acquire_card in Move state {}".format(self.current_move.state))
        if self.current_move.card_source == CardSource.DRAW_STACK:
            self.current_move.acquired = self._draw()
        elif self.current_move.card_source == CardSource.DISCARD_STACK:
            self.current_move.acquired = self._draw_discard()

    def _do_turn(self):
        """Interact with a Player to make a Move.

        Side effects:
         * gives player card via the acquired property of the Move
         * calls pre_turn_hook and post_turn_hook
        """
        self.pre_turn_hook()
        self.start_new_move()
        self._current_player.turn_start(self.current_move)
        self.acquire_card()

        self._current_player.turn_finish(self.current_move)

        if self.current_move.knocking is True:
            #### game is ending
            # FIXME: validate meld legitimacy
            # FIXME: check for super-gin
            # FIXME: deal with deadwood in non-gin knock scenario
            self._knocked = True
            print("{} wins".format(self._current_player))
            return

        assert self.current_move.state == MoveState.COMPLETE
        self._discards.add(self.current_move.discarded)
        self.post_turn_hook()

    def play(self) -> None:
        """Play a game by alternating moves until one player knocks."""
        while True:
            self.start_new_move()
            self._do_turn()
            if self.current_move.knocking is True:
                print("{} has knocked to end the game".
                      format(self._current_player))
                # FIXME - add validity checking & scoring
                break
            self._alternate_player()

    def status_for(self, player) -> dict:
        """Return a game status structure for the specified player.

        The game status structure consists of:

        game_id: UUID of the game
        desription: string describing game
        current_player: UUID of player taking current turn
        [visible_discard:]
         - suit: string form of suit enum
         - card: string form of card enum
        [new_card:]
         - suit: string form of suit enum
         - card: string form of card enum
        hand: list of suit,card objects

        This is a conveniennce for the benefit of UIs and other
        game management logic.

        (Note: all UUIDs are in string form.)
        """
        if player not in (self.player1, self.player2):
            raise PylgrumInternalError("Can't generate game status for uninvolved player")

        r = {
            "game_id": self.game_id,
            "description": "game between {} and {}".format(
                self.player1.contestant_id,
                self.player2.contestant_id,
            ),
            "current_player": self._current_player.contestant_id,
        }
        try:
            visible_discard = self.visible_discard
        except CardNotFoundError:
            r['visible_discard'] = {
                'suit': "",
                'card': ""
            }
        else:
            r['visible_discard'] = {
                'suit': str(visible_discard.suit),
                'card': str(visible_discard.rank)
            }
        ## only the curent player can see the acquired card
        if self.current_player == player:
            if (self.current_move is not None and
                self.current_move.acquired is not None):
                r['new_card'] = {
                    'suit': str(self.current_move.acquired.suit),
                    'card': str(self.current_move.acquired.rank)
                }
        r['hand'] = [{"suit": str(x.suit), "rank": str(x.rank)} for x in player.hand.cards]
        return r
