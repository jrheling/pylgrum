"""Controller for game of gin rummy."""

from pylgrum.player import Player
from pylgrum.move import Move, CardSource, MoveState
from pylgrum.deck import Deck
from pylgrum.card import Card
from pylgrum.stack import CardStack
from pylgrum.errors import IllegalMoveError, PylgrumInternalError, CardNotFoundError

class Game():
    """Base class for a game of gin rummy.

    A game consists of a series of moves between two players. The Game object
    is responsible for managing game state, including turn order between
    the players and the exchange of cards.

    Depending on subclass behavior, game play can proceed in two different
    modes:

        *synchronously*: where the Game drives play through the callbacks
        to the Players (via the `*_hook()` methods below)

        *asynchronously*: where Players submit moves (e.g. via the API) and
        the Game enforces move validity and game state

    The only real difference between the two modes is that the async player
    is expected to track game state enough to know when to move. (Note that even
    in this mode the player is not _trusted_ by the game - game still enforces
    move validity.)

    Most interactive usage is probably best served by the asynchronous mode,
    though synchronous mode might be useful for e.g. machine-driven training.
    """

    def __init__(self, player1: Player, player2: Player, game_id: str = None) -> None:
        """Create a new game between two players.

        Shuffles and deals a deck, and starts play.

        Args:
            player1 (Player): the player initiating the game
            player2 (Player): the player being challenged
            game_id (str): [optional] an ID used to track this game

        If not provided, game_id will be None.
        """

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
        """The player whose turn it currently is."""
        return self._current_player

    @property
    def visible_discard(self):
        """The card currently showing on the top of the discard pile."""
        return self._discards.peek()

    @property
    def contestant_ids(self):
        """A list of contestant IDs for the players in this game."""
        return [p.contestant_id for p in [self.player1, self.player2]]

    def _draw(self) -> Card:
        """Draw from the deck."""
        return self._deck.draw()

    def _draw_discard(self) -> Card:
        """Take the visible discarded card."""
        return self._discards.draw()

    def next_turn(self) -> None:
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
            raise PylgrumInternalError("No current_player?!")

    def pre_turn_hook(self):
        """Called before each move. For sub-class use."""

    def post_turn_hook(self):
        """Called after each move. For sub-class use."""

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

        Before this method is called, the `current_move` should indicate
        whether the current player has chosen to take the discard or a new
        card from the deck. This method moves the chosen card into the player's
        hand.

        Raises IllegalMoveError if called before the card source has been chosen.
        """
        if self.current_move.state != MoveState.IN_PROGRESS:
            raise IllegalMoveError(
                "Got to _acquire_card in Move state {}"
                .format(self.current_move.state)
            )
        if self.current_move.card_source == CardSource.DRAW_STACK:
            self.current_move.acquired = self._draw()
        elif self.current_move.card_source == CardSource.DISCARD_STACK:
            self.current_move.acquired = self._draw_discard()
        self.current_player.receive_card(self.current_move.acquired)

    def finalize_move(self) -> None:
        """Complete a move by processing the specified discard.

        Before this method is called, the `current_move` should indicate which
        card the current player has chosen to discard. This method actually
        removes it from their hand and adds it to the discard pile.

        Raises IllegalMoveError if called for a move that is not complete.
        """
        if self.current_move.state != MoveState.COMPLETE:
            raise IllegalMoveError(
                "Got to finalize_move in Move state {}"
                .format(self.current_move.state)
            )
        if not self.current_move.discard:
            raise IllegalMoveError("No discard specified.")

        try:
            discard_idx = self.current_player.hand.find(self.current_move.discarded)
        except CardNotFoundError:
            raise IllegalMoveError("Specified discard not in player's hand.")
        else:
            self.current_player.hand.remove(discard_idx)
            self._discards.add(self.current_move.discarded)

    def _do_turn(self):
        self.pre_turn_hook()
        self.start_new_move()
        self._current_player.turn_start(self.current_move)
        self.acquire_card()

        self._current_player.turn_finish(self.current_move)
        self.finalize_move()

        if self.current_move.knocking is True:
            #### game is ending
            # FIXME: validate meld legitimacy
            # FIXME: check for super-gin
            # FIXME: deal with deadwood in non-gin knock scenario
            self._knocked = True
            print("{} wins".format(self._current_player))
            return

        assert self.current_move.state == MoveState.COMPLETE
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
            self.next_turn()

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

        This is a convenience method for the benefit of UIs and other
        game management logic.

        (Note: all UUIDs are in string form.)
        """
        if player not in (self.player1, self.player2):
            raise PylgrumInternalError(
                "Can't generate game status for uninvolved player"
            )

        r_val = {
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
            r_val['visible_discard'] = {
                'suit': "",
                'card': ""
            }
        else:
            r_val['visible_discard'] = {
                'suit': visible_discard.suit.name,
                'card': visible_discard.rank.name
            }
        ## only the curent player can see the acquired card
        if self.current_player == player:
            if (self.current_move is not None and
                    self.current_move.acquired is not None):
                r_val['new_card'] = {
                    'suit': self.current_move.acquired.suit.name,
                    'card': self.current_move.acquired.rank.name
                }
        r_val['hand'] = [{"suit": x.suit.name, "card": x.rank.name} for x in player.hand.cards]
        return r_val
