import unittest
from unittest import skip
from pylgrum.move import Move, MoveState, CardSource
from pylgrum.card import Card, Rank, Suit
from pylgrum.errors import IllegalMoveError

class TestMove(unittest.TestCase):

    def setUp(self):
        self.m = Move(Card(rank=Rank.QUEEN, suit=Suit.CLUB))

    def test_move_init(self):
        self.assertEqual(self.m.state, MoveState.NEW)
        self.assertEqual(self.m.card_source, None)
        self.assertEqual(self.m.acquired, None)
        self.assertEqual(self.m.discarded, None)
        self.assertEqual(self.m.knocking, False)
        self.assertEqual(str(self.m), "(move still in progress)")

    def test_draw(self):
        self.m.choose_card_from_draw()
        self.assertEqual(self.m.state, MoveState.IN_PROGRESS)
        self.assertEqual(self.m.card_source, CardSource.DRAW_STACK)

    def test_choose_card_from_discard(self):
        self.m.choose_card_from_discard()
        self.assertEqual(self.m.state, MoveState.IN_PROGRESS)
        self.assertEqual(self.m.card_source, CardSource.DISCARD_STACK)

    def test_double_draw(self):
        self.m.choose_card_from_draw()
        with self.assertRaises(IllegalMoveError):
            self.m.choose_card_from_draw()

    def test_draw_and_discard(self):
        self.m.choose_card_from_draw()
        with self.assertRaises(IllegalMoveError):
            self.m.choose_card_from_discard()

    def test_double_discard(self):
        self.m.choose_card_from_discard()
        with self.assertRaises(IllegalMoveError):
            self.m.choose_card_from_discard()

    def test_early_discard(self):
        with self.assertRaises(IllegalMoveError):
            self.m.discard(Card(rank=Rank.QUEEN, suit=Suit.HEART))

if __name__ == '__main__':
    unittest.main()
