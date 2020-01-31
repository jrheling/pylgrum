import pytest

from pylgrum.card import Card, Rank, Suit
from pylgrum.hand import Hand
from pylgrum.meld import Meld
from pylgrum.meld_detector import MeldDetector
from pylgrum.errors import InvalidMeldError

@pytest.fixture
def hand_with_simple_runs():
    """A simple, same-suit, in-order hand with two runs.

    Should find two runs:
        (JH, QH, KH)
        (AS, 2S, 3S)
    """
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))    # 0:  JH
    hand.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))   # 1:  QH
    hand.add(Card(rank=Rank.KING, suit=Suit.HEART))    # 2:  KH
    hand.add(Card(rank=Rank.KING, suit=Suit.SPADE))    # 3:  KS
    hand.add(Card(rank=Rank.TWO, suit=Suit.HEART))     # 4:  2H
    hand.add(Card(rank=Rank.THREE, suit=Suit.DIAMOND)) # 5:  3D
    hand.add(Card(rank=Rank.ACE, suit=Suit.SPADE))     # 6:  AS
    hand.add(Card(rank=Rank.TWO, suit=Suit.SPADE))     # 7:  2S
    hand.add(Card(rank=Rank.THREE, suit=Suit.SPADE))   # 8:  3S
    hand.add(Card(rank=Rank.NINE, suit=Suit.DIAMOND))  # 9:  9D

    yield hand

@pytest.fixture
def hand_with_complex_runs():
    """Multiple suits, not in order, overlapping runs

    Should find 7 runs:
        (3H, 4H, 5H),
        (4H, 5H, 6H),
        (5H, 6H, 7H),
        (3H, 4H, 5H, 6H),
        (4H, 5H, 6H, 7H),
        (3H, 4H, 5H, 6H, 7H),
        (9C, 10C, JC)
    """
    hand = Hand()

    hand.add(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
    hand.add(Card(rank=Rank.ACE, suit=Suit.HEART))
    hand.add(Card(rank=Rank.THREE, suit=Suit.HEART))
    hand.add(Card(rank=Rank.SEVEN, suit=Suit.HEART))
    hand.add(Card(rank=Rank.FOUR, suit=Suit.HEART))
    hand.add(Card(rank=Rank.SIX, suit=Suit.HEART))
    hand.add(Card(rank=Rank.JACK, suit=Suit.CLUB))
    hand.add(Card(rank=Rank.FIVE, suit=Suit.HEART))
    hand.add(Card(rank=Rank.TEN, suit=Suit.SPADE))
    hand.add(Card(rank=Rank.NINE, suit=Suit.CLUB))
    hand.add(Card(rank=Rank.TEN, suit=Suit.CLUB))

    yield hand

def test_new_meld_detector_with_no_cards():
    md = MeldDetector()
    assert(isinstance(md, MeldDetector))
    assert(md.size() == 0)

def test_new_meld_detector_init_from_hand(hand_with_simple_runs):
    md = MeldDetector(*hand_with_simple_runs.cards)
    assert(isinstance(md, MeldDetector))
    assert(md.size() == 10)

def test_add_clears_detect_flag(hand_with_simple_runs):
    md = MeldDetector(*hand_with_simple_runs.cards)
    md._detect_all_melds()
    md.add(Card(rank=Rank.SIX, suit=Suit.CLUB))
    assert(md._detected == False)

def test_deadwood_count_is_correct():
    """implement"""

def test_deadwood_value_is_correct():
    """implement"""

def test_small_hand_is_not_complete():
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))    # 0:  JH
    hand.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))   # 1:  QH

    md = MeldDetector(*hand.cards)
    assert(md.is_complete_hand == False)

def test_correctly_sized_hand_is_complete(hand_with_simple_runs):
    md = MeldDetector(*hand_with_simple_runs.cards) # 10 cards
    assert(md.is_complete_hand == True)
    md.add(Card(rank=Rank.SIX, suit=Suit.CLUB)) # 11 is ok, too
    assert(md.is_complete_hand == True)

def test_simple_run_detection(hand_with_simple_runs):
    """'simple' here means each run sequence is only 3 long, so no overlap"""
    md = MeldDetector(*hand_with_simple_runs.cards)
    md._find_runs()
    assert(len(md._melds) == 2)

def test_complex_run_detection(hand_with_complex_runs):
        # (3H, 4H, 5H),
        # (4H, 5H, 6H),
        # (5H, 6H, 7H),
        # (3H, 4H, 5H, 6H),
        # (4H, 5H, 6H, 7H),
        # (3H, 4H, 5H, 6H, 7H),
        # (9C, 10C, JC)
    expected_melds = [
        Meld(Card.from_text("3H", "4H", "5H")),
        Meld(Card.from_text("4H", "5H", "6H")),
        Meld(Card.from_text("5H", "6H", "7H")),
        Meld(Card.from_text("3H", "4H", "5H", "6H")),
        Meld(Card.from_text("4H", "5H", "6H", "7H")),
        Meld(Card.from_text("3H", "4H", "5H", "6H", "7H")),
        Meld(Card.from_text("9C", "10C", "JC"))
    ]
    md = MeldDetector(*hand_with_complex_runs.cards)
    md._find_runs()
    assert(len(md._melds) == 7)
    for meld in expected_melds:
        assert(meld in md._melds)

def test_runs_must_be_three_long_to_count():
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))    # 0:  JH
    hand.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))   # 1:  QH

    md = MeldDetector(*hand.cards)
    md._find_runs()
    assert(len(md._melds) == 0)

def test_runs_must_be_same_suit():
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))
    hand.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))
    hand.add(Card(rank=Rank.KING, suit=Suit.CLUB))

    md = MeldDetector(*hand.cards)
    md._find_runs()
    assert(len(md._melds) == 0)

def test_():
    """implement"""

## FIXME - copy run tests for sets once they're working

## FIXME - add optimal meld detection
