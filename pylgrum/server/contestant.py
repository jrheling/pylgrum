"""The Contestant class represents an agent that might play games.

The difference between Contestant and Player is perhaps non-obvious.

The Player class represents to a player _in a specific game_, whereas Contestant
is the entity (person, bot, etc.) who might be behind one or more Players.

For example: Esmerelda (a human) plays 3 games of Gin Rummy one day via an instance
of GameManager. In each of the three games, there is a Player object that represents
Esmerelda's side of the game. There is, additionally, a single Contestant object
that represents Esmerelda.
"""

import uuid
import json

from pylgrum.player import Player

from pylgrum.server.errors import ContestantAlreadyPlaying

class Contestant():
    """A Contestant is an entity that might play games."""
    _DEFAULT_NAME = "Anon Y. Mouse"

    def __init__(self, name=None):
        """Create and initialize a Contestant.

        Args:
            name (str): [optional] A display-appropriate identifier for the contestant

        If not defined or specified as None, name is initialized to _DEFAULT_NAME.
        """
        self.current_player = None
        self.id = str(uuid.uuid4()) #pylint: disable=invalid-name
        self.name = name if name else Contestant._DEFAULT_NAME

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
        """Return a Player object so a game can be started.

        Note: the Player will reference a Game it has been joined to, so a Contestant
        instance can access any Game it is part of.
        """
        if self.is_playing:
            raise ContestantAlreadyPlaying
        self.current_player = Player(contestant_id=self.id)
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
