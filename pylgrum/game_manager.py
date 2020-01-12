"""The GameManager class manages muliple games between multiple users."""

import uuid
import json

from pylgrum import Player, Game

# Note: "Player" refers to a player _in a specific game_, so would be a confusing
# term to refer to the humans or bots who might play on a GameServer.
class Contestant():
    DEFAULT_NAME = "Anon Y. Mouse"

    class ContestantAlreadyPlaying(Exception):
        """Raised when a Contestant tries to join a Game with one in progress."""
        pass

    """A Contestant is an entity that might play games."""
    def __init__(self, name = None):
        self.current_player = None
        self.id = str(uuid.uuid4())
        self.name = name if name else Contestant.DEFAULT_NAME

    @property
    def is_playing(self):
        """True if the Contestant is in a game, or in the process of joining one.

        Note: There is a moment after join_game() has been called when the Contestant
        might not actually be in a game yet, but has agreed to join one (this moment)
        is while the game is being created. In the future we could express a "pending"
        state here, but for now this is considered "playing".
        """
        return self.current_player is not None

    def join_game(self):
        """Returns a Player object so a game can be started.

        Note: the Player will reference a Game it has been joined to, so a Contestant
        instance can access any Game it is part of.
        """
        if self.is_playing:
            raise Contestant.ContestantAlreadyPlaying
        self.current_player = Player(contestant_id = self.id)
        return self.current_player

    def __str__(self):
        """Returns JSON with public members (e.g. for API return)."""
        # Skipping certain fields (e.g. those with leading _) is surprisingly
        #  involved, so for now just hand-write the JSON. Definite room for future
        #  improvement
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "currently_playing": self.is_playing
        })

class GameManager():
    """A GameManager handles a pool of Contestants and a number of Games."""

    class InvalidContestant(Exception):
        """Raised for non-existant or invalid Contestants."""
        pass

    def __init__(self):
        self.contestants = {}
        self.games = {}

    def list_contestants(self):
        # return [str(self._contestants[c]) for c in self._contestants.keys()]
        return [
            {
                "id": c.id,
                "name": c.name,
                "currently_playing": c.is_playing
            }
            for c in self.contestants.values()
        ]

    def delete_contestants(self):
        self.contestants = {}

    def add_contestant(self, name = None):
        """Create and return new contestant with given name.

        Note: uses default name from Contestant class if no name given.
        """
        new_contestant = Contestant(name)
        self.contestants[new_contestant.id] = new_contestant
        return new_contestant

    def create_game(self, challenger_id: str, opponent_id: str):
        """Create a game between specified players.

        Takes:
         * challenger_id: str of UUID of player starting the game
         * opponent_id: str of UUID of the other player

        Note: both players must be registered contestants who are not already
        in a game.
        """
        if challenger_id not in self.contestants.keys():
            raise GameManager.InvalidContestant("Invalid challenger")
        if opponent_id not in self.contestants.keys():
            raise GameManager.InvalidContestant("Invalid opponent")

        p1 = self.contestants[challenger_id]
        p2 = self.contestants[opponent_id]

        new_game_id = str(uuid.uuid4())
        new_game = Game(p1.join_game(), p2.join_game(), game_id=new_game_id)

        self.games[new_game_id] = new_game

        return(
            {
                "description": "Game between {} and {}".format(p1.name, p2.name),
                "id": new_game_id
            }
        )

