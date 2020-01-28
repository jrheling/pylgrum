"""Errors for pylgrum.server"""

from pylgrum.errors import PylgrumError

class ContestantAlreadyPlaying(PylgrumError):
    """Raised when a Contestant tries to join a Game with one in progress."""
    pass

class InvalidContestant(PylgrumError):
    """Raised for non-existant or invalid Contestants."""
    pass