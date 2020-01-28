"""Errors for the pylgrum package."""

class PylgrumError(Exception):
    """Base class for this module's exceptions."""

class PylgrumErrorWithMessage(PylgrumError):
    """Base class with exception message."""
    def __init__(self, message = None):
        self.message = message
        super().__init__()

class PylgrumInternalError(PylgrumErrorWithMessage):
    """Catch-all for low-level errors."""

class CardNotFoundError(PylgrumErrorWithMessage):
    """Raised when a card isn't found in a Stack."""
    def __init__(self, message):
        self.message = message
        super().__init__()

class OverdealtHandError(PylgrumError):
    """Raised when a hand would otherwise end up with >11 cards.

    Note: a hand has 10 cards, but will briefly hold 11 during a turn.
    """

class IllegalMoveError(PylgrumErrorWithMessage):
    """Raised when a Player does something illegal in a move.

    For example: asking a Move to draw after already asking to draw a
    discard would result in IllegalMoveError.
    """

class InvalidMeldError(PylgrumErrorWithMessage):
    """Raised when a meld or potential meld that isn't either all the same
    suit or all the same rank is encountered."""
