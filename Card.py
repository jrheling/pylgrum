#!/usr/bin/python

# PEP-008 training wheels
#0123456789012345678901234567890123456789012345678901234567890123456789012345678

# std lib imports
#
# related 3rd party imports
#
# local ipmorts

from enum import Enum

"""Trivial enum of card suits."""
class Suit(Enum):
    SPADE = 'S'
    HEART = 'H'
    CLUB = 'C'
    DIAMOND = 'D'

"""Simple class to track card ranks (e.g. ace, face cards, royals, etc.).

Public methods:
 score_val() - returns point value for cards of that rank.
"""
class Rank(Enum):
    ACE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'

    def score_val(self) -> int:
        """Return the point value of a card (if held as 'deadwood')."""
        if self.name is "A":
            return 1
        elif self.name in ("JACK","QUEEN","KING"):
            return 10
        else:
            return int(self.value)


"""Cards have suit+rank, point value, and can be compared (by point value).

Public methods:
 __init__(suit, rank)
 overriden operators ==, !=, <, >, <=, >= work on point value (e.g. Jack == King)
"""
class Card:
    suit: Suit = None
    rank: Rank = None

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other) -> bool:
        return self.rank.score_val() == other.rank.score_val()
        
    def __ne__(self, other) -> bool:
        return self.rank.score_val() != other.rank.score_val()
        
    def __lt__(self, other) -> bool:
        return self.rank.score_val() < other.rank.score_val()
        
    def __le__(self, other) -> bool:
        return self.rank.score_val() <= other.rank.score_val()
        
    def __gt__(self, other) -> bool:
        return self.rank.score_val() > other.rank.score_val()
        
    def __ge__(self, other) -> bool:
        return self.rank.score_val() >= other.rank.score_val()
        