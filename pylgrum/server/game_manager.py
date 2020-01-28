"""The GameManager class manages muliple games between multiple users."""

import uuid

from pylgrum.game import Game
from pylgrum.server.contestant import Contestant

from pylgrum.server.errors import InvalidContestant

class GameManager():
    """A GameManager handles a pool of Contestants and a number of Games."""

    def __init__(self):
        """Initialize a new GameManger."""
        self.contestants = {}
        self.games = {}

    def list_contestants(self):
        """Return a list of JSON objects representing currently registered contestants."""
        return [
            {
                "id": c.id,
                "name": c.name,
                "currently_playing": c.is_playing
            }
            for c in self.contestants.values()
        ]

    def delete_contestants(self):
        """Clears the set of registered contestants.

        Use with caution: this is primarily of value in unit tests.
        """
        self.contestants = {}

    def add_contestant(self, name=None):
        """Create and return new contestant with given name.

        Args:
            name (str): [optional] name of the new contestant

        Note: uses default name from Contestant class if no name given.
        """
        new_contestant = Contestant(name)
        self.contestants[new_contestant.id] = new_contestant
        return new_contestant

    def create_game(self, challenger_id: str, opponent_id: str):
        """Create a game between specified players.

        Args:
            challenger_id (str): UUID of player starting the game
            opponent_id (str): UUID of the other player

        Raises InvalidContestant unless both players are registered contestants who
        are not already in a game.
        """
        if challenger_id not in self.contestants.keys():
            raise InvalidContestant("Invalid challenger")
        if opponent_id not in self.contestants.keys():
            raise InvalidContestant("Invalid opponent")

        player1 = self.contestants[challenger_id]
        player2 = self.contestants[opponent_id]

        new_game_id = str(uuid.uuid4())
        new_game = Game(player1.join_game(), player2.join_game(), game_id=new_game_id)

        self.games[new_game_id] = new_game

        return(
            {
                "description": "Game between {} and {}".format(player1.name, player2.name),
                "id": new_game_id
            }
        )
