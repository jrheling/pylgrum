import pytest

from pylgrum.card import Card, Rank, Suit
from pylgrum.hand import Hand
from pylgrum.meld import Meld
from pylgrum.meld_detector import MeldDetector
from pylgrum.errors import InvalidMeldError


COMPLEX_OPTIMIZATION_UNIMP=True

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
def hand_with_sets():
    """A hand with two sets.

    Should find 6 sets:
        (QH, QC, QD)
        (2S, 2H, 2D, 2C) - 5 permutations of this
    """
    hand = Hand()
    for card in Card.from_text(
        "JH", "QH", "QC", "QD", "2S",
        "3C", "2H", "6S", "2D", "2C"
    ):
        hand.add(card)

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

@pytest.fixture
def hand_with_simple_sets_and_runs():
    """A hand with non-overlapping sets and runs.

    Should find 6 melds:
        2C 2S 2H  (1 set)
        4D 5D 6D  (1 run)
        9S 10S JS (1 set)
        4C

    This hand should have 4 points of deadwood (1 deadwood card)
    """
    hand = Hand()
    for card in Card.from_text(
        "2C", "2S", "2H", "4D", "5D",
        "6D", "9S", "10S", "JS", "4C"
    ):
        hand.add(card)

    yield hand


@pytest.fixture
def hand_with_overlapping_sets_and_runs():
    """A hand with obviously overlapping sets and runs.

    Should find 6 melds:
        2C 2S 2H 2D (5 permutations of set)
        4D 5D 6D    (1 run)
        8S
        10S
        JS

    This hand should have 28 points of deadwood (3 deadwood cards)

    The optimal sets from this hand are:
        2C 2S 2H 2D
        4D 5D 6D
    """
    hand = Hand()
    for card in Card.from_text(
        "2C", "2S", "2H", "2D", "4D", "5D", "6D", "8S", "10S", "JS"
    ):
        hand.add(card)

    yield hand

@pytest.fixture
def hand_with_complex_sets_and_runs():
    """A hand with overlapping sets and runs.

    Should find 10 melds:
        2C 2S 2H 2D (5 permutations of set)
        3D 4D 5D    (3 perms of run (including 2 above): 234, 345, 2345)
        3S          (1 set - 333)
        3C AC       (1 run - A23 (2 is above))

    This hand should have 0 points of deadwood (0 deadwood cards)
    """
    hand = Hand()
    for card in Card.from_text(
        "2C", "2S", "2H", "2D",
        "3D", "4D", "5D", "3S",
        "3C", "AC"
    ):
        hand.add(card)

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
    md._detect_all_melds()
    assert(len(md._melds) == 2)

def test_simple_set_detection(hand_with_sets):
    md = MeldDetector(*hand_with_sets.cards)
    md._detect_all_melds()
    assert(len(md._melds) == 6)

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
    md._detect_all_melds()
    assert(len(md._melds) == 7)
    for meld in expected_melds:
        assert(meld in md._melds)

def test_runs_must_be_three_long_to_count():
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))    # 0:  JH
    hand.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))   # 1:  QH

    md = MeldDetector(*hand.cards)
    md._detect_all_melds()
    assert(len(md._melds) == 0)

def test_sets_must_be_three_long_to_count():
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))    # 0:  JH
    hand.add(Card(rank=Rank.JACK, suit=Suit.DIAMOND))   # 1:  JD

    md = MeldDetector(*hand.cards)
    md._detect_all_melds()
    assert(len(md._melds) == 0)

def test_runs_must_be_same_suit():
    hand = Hand()

    hand.add(Card(rank=Rank.JACK, suit=Suit.HEART))
    hand.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))
    hand.add(Card(rank=Rank.KING, suit=Suit.CLUB))

    md = MeldDetector(*hand.cards)
    md._detect_all_melds()
    assert(len(md._melds) == 0)

def test_set_and_run_detection(hand_with_overlapping_sets_and_runs):
    expected_melds = [
        Meld(Card.from_text("2C", "2S", "2D", "2H")),
        Meld(Card.from_text("2S", "2D", "2H")),
        Meld(Card.from_text("2C", "2D", "2H")),
        Meld(Card.from_text("2C", "2S", "2H")),
        Meld(Card.from_text("2C", "2S", "2D")),
        Meld(Card.from_text("4D", "5D", "6D"))
    ]
    md = MeldDetector(*hand_with_overlapping_sets_and_runs.cards)
    md._detect_all_melds()
    assert(len(md._melds) == 6)
    for meld in expected_melds:
        assert(meld in md._melds)

def test_deadwood_count_is_correct_from_simple_hand(hand_with_simple_sets_and_runs):
    md = MeldDetector(*hand_with_simple_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(md.optimal_hand.deadwood_count == 1)

def test_deadwood_value_is_correct_from_simple_hand(hand_with_simple_sets_and_runs):
    md = MeldDetector(*hand_with_simple_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(md.optimal_hand.deadwood_value == 4)

def test_deadwood_count_is_correct_from_overlapping_hand(hand_with_overlapping_sets_and_runs):
    md = MeldDetector(*hand_with_overlapping_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(md.optimal_hand.deadwood_count == 3)

def test_deadwood_value_is_correct_from_overlapping_hand(hand_with_overlapping_sets_and_runs):
    md = MeldDetector(*hand_with_overlapping_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(md.optimal_hand.deadwood_value == 28)

def test_overlapping_set_and_run_detection(hand_with_complex_sets_and_runs):
    expected_melds = [
        Meld(Card.from_text("2C", "2S", "2D", "2H")),
        Meld(Card.from_text("2S", "2D", "2H")),
        Meld(Card.from_text("2C", "2D", "2H")),
        Meld(Card.from_text("2C", "2S", "2H")),
        Meld(Card.from_text("2C", "2S", "2D")),

        Meld(Card.from_text("2D", "3D", "4D")),
        Meld(Card.from_text("3D", "4D", "5D")),
        Meld(Card.from_text("2D", "3D", "4D", "5D")),

        Meld(Card.from_text("3D", "3S", "3C")),

        Meld(Card.from_text("AC", "2C", "3C")),
    ]
    md = MeldDetector(*hand_with_complex_sets_and_runs.cards)
    md._detect_all_melds()
    assert(len(md._melds) == 10)
    for meld in expected_melds:
        assert(meld in md._melds)

def test_optimal_melds_chosen_from_simple_hand(hand_with_simple_sets_and_runs):
    expected_melds = [
        Meld(Card.from_text("2C", "2S", "2H")),
        Meld(Card.from_text("9S", "10S", "JS")),
        Meld(Card.from_text("4D", "5D", "6D"))
    ]
    md = MeldDetector(*hand_with_simple_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(len(md.optimal_hand.melds) == 3)
    for meld in expected_melds:
        assert(meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_count == 1)
    assert(md.optimal_hand.deadwood_value == 4)

def test_optimal_melds_chosen_from_hand_with_overlapping_melds(hand_with_overlapping_sets_and_runs):
    expected_melds = [
        Meld(Card.from_text("2C", "2S", "2D", "2H")),
        Meld(Card.from_text("4D", "5D", "6D"))
    ]
    md = MeldDetector(*hand_with_overlapping_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(len(md.optimal_hand.melds) == 2)
    for meld in expected_melds:
        assert(meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_count == 3)
    assert(md.optimal_hand.deadwood_value == 28)

def test_optimal_melds_chosen_from_complex_set(hand_with_complex_sets_and_runs):
    expected_melds = [
        Meld(Card.from_text("2D", "2S", "2H")),
        Meld(Card.from_text("3D", "4D", "5D")),
        Meld(Card.from_text("AC", "2C", "3C"))
    ]
    md = MeldDetector(*hand_with_complex_sets_and_runs.cards)
    md.detect_optimal_melds()
    assert(len(md.optimal_hand.melds) == 3)
    for meld in expected_melds:
        assert(meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 3)

def test_optimal_meld_scenario_1():
    h = Hand()
    for card in Card.from_text(
        "10S", "9S", "8S",
        "8H",
        "9C", "8C", "7C", "6C", "5C",
        "KD"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("10S", "9S", "8S")),
        Meld(Card.from_text("9C", "8C", "7C", "6C", "5C"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 18)
    assert(md.optimal_hand.deadwood_count == 2)

def test_optimal_meld_scenario_2():
    h = Hand()
    for card in Card.from_text(
        "10S", "9S", "8S",
        "9H", "8H",
        "9C", "8C", "7C",
        "9D",
        "QD"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("9S", "9H", "9C", "9D")),
        Meld(Card.from_text("8S", "8H", "8C"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 27)
    assert(md.optimal_hand.deadwood_count == 3)

def test_optimal_meld_scenario_3():
    h = Hand()
    for card in Card.from_text(
        "10S", "9S", "8S",
        "9H", "8H",
        "9C", "8C", "7C",
        "9D",
        "JS"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("9H", "9C", "9D")),
        Meld(Card.from_text("8H", "8C", "8S")),
        Meld(Card.from_text("9S", "10S", "JS"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 7)
    assert(md.optimal_hand.deadwood_count == 1)

def test_optimal_meld_scenario_4():
    h = Hand()
    for card in Card.from_text(
        "10S", "9S", "8S",
        "9H", "8H",
        "9C", "8C", "7C",
        "9D",
        "8D"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("8S", "9S", "10S")),
        Meld(Card.from_text("8H", "8C", "8D")),
        Meld(Card.from_text("8H", "8C", "8D"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 7)
    assert(md.optimal_hand.deadwood_count == 1)

def test_optimal_meld_scenario_5():
    h = Hand()
    for card in Card.from_text(
        "10S", "9S", "8S",
        "9H", "8H",
        "9C", "8C", "7C",
        "9D",
        "6C"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("9H", "9C", "9D")),
        Meld(Card.from_text("6C", "7C", "8C")),
        Meld(Card.from_text("8S", "9S", "10S"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 8)
    assert(md.optimal_hand.deadwood_count == 1)

def test_optimal_meld_scenario_6():
    h = Hand()
    for card in Card.from_text(
        "4S", "3S", "2S", "AS",
        "3H", "2H", "AH",
        "4D", "3D", "2D"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("4S", "3S", "2S", "AS")),
        Meld(Card.from_text("3H", "2H", "AH")),
        Meld(Card.from_text("4D", "3D", "2D"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 0)
    assert(md.optimal_hand.deadwood_count == 0)

def test_optimal_meld_scenario_7():
    h = Hand()
    for card in Card.from_text(
        "4C",
        "4S", "3S", "2S",
        "4H", "3H", "2H", "AH",
        "3D", "2D"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("4C", "4S", "4H")),
        Meld(Card.from_text("3H", "3S", "3D")),
        Meld(Card.from_text("2H", "2S", "2D"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 1)
    assert(md.optimal_hand.deadwood_count == 1)

# @pytest.mark.skipif(COMPLEX_OPTIMIZATION_UNIMP, reason="not ready yet")
def test_optimal_meld_scenario_8():
    h = Hand()
    for card in Card.from_text(
        "4C",
        "4S", "3S", "2S",
        "5H", "4H", "3H", "AH",
        "3D", "2D"
    ):
        h.add(card)

    ## in this scenario, there are two equally optimal outcomes
    optimal_expected_option1 = [
        Meld(Card.from_text("4C", "4S", "4H")),
        Meld(Card.from_text("3H", "3S", "3D"))
    ]
    optimal_expected_option2 = [
        Meld(Card.from_text("4S", "3S", "2S")),
        Meld(Card.from_text("5H", "4H", "3H"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected_option1)) # works for either

    is_option_1 = True
    is_option_2 = True

    for expected_meld in optimal_expected_option1:
        if expected_meld not in md.optimal_hand.melds:
            is_option_1 = False

    for expected_meld in optimal_expected_option2:
        if expected_meld not in md.optimal_hand.melds:
            is_option_2 = False

    assert(not (is_option_1 and is_option_2)) #highlander principle
    assert(is_option_1 or is_option_2)

    # b/c the two are equiv. this is true regardless of option
    assert(md.optimal_hand.deadwood_value == 10)
    assert(md.optimal_hand.deadwood_count == 4)

def test_optimal_meld_scenario_9():
    # this is a relatively simple scenario - only one card is overused
    h = Hand()
    for card in Card.from_text(
        "6D", "6C", "6H",
        "2H", "3H", "4H",
        "2S", "2C"
    ):
        h.add(card)

    optimal_expected = [
        Meld(Card.from_text("6D", "6C", "6H")),
        Meld(Card.from_text("2H", "3H", "4H"))
    ]
    md = MeldDetector(*h.cards)
    md.detect_optimal_melds()

    assert(len(md.optimal_hand.melds) == len(optimal_expected))
    for expected_meld in optimal_expected:
        assert(expected_meld in md.optimal_hand.melds)
    assert(md.optimal_hand.deadwood_value == 4)
    assert(md.optimal_hand.deadwood_count == 2)

def test_(hand_with_complex_sets_and_runs):
    """foo"""

