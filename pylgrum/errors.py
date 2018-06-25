"""Errors for the pylgrum package."""

class PylgrumError(Exception):
    """Base class for this module's exceptions."""
    pass

class CardNotFoundError(PylgrumError):
    """Raised when a card isn't found in a stack (or stack subclass)."""
    def __init__(self, message):
        self.message = message
        super().__init__()
