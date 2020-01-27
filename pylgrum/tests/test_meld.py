import unittest
from unittest import skip
from pylgrum.meld import Meld
from pylgrum.card import Card, Suit, Rank
from pylgrum.errors import InvalidMeldError

class TestMeld(unittest.TestCase):

    def test_same_suit(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.SIX, suit=Suit.HEART))
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_not_same_suit(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.TWO, suit=Suit.CLUB))
        self.assertFalse(m.all_same_suit)
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_same_rank(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_not_same_rank(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.THREE, suit=Suit.HEART))
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_partial_run(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.THREE, suit=Suit.HEART))
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_full_run(self):
        # these cards are intentionally out of order - order is not
        #  reliable for cards added at init time
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.FOUR, suit=Suit.HEART),
                 Card(rank=Rank.THREE, suit=Suit.HEART))
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.is_run)
        self.assertFalse(m.is_set)
        self.assertTrue(m.complete)

    def test_add_sorts(self):
        c2 = Card(rank=Rank.TWO, suit=Suit.CLUB)
        c3 = Card(rank=Rank.THREE, suit=Suit.CLUB)
        c4 = Card(rank=Rank.FOUR, suit=Suit.CLUB)

        m = Meld(c2)
        m.add(c4)
        m.add(c3)
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.all_same_suit)
        self.assertTrue(m.is_run)
        self.assertFalse(m.is_set)
        self.assertTrue(m.complete)

        # cards were implicitly re-ordered by add()
        self.assertEqual(m.cards[0],c2)
        self.assertEqual(m.cards[1],c3)
        self.assertEqual(m.cards[2],c4)

    def test_partial_set(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_full_set(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.TWO, suit=Suit.CLUB),
                 Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertTrue(m.is_set)
        self.assertTrue(m.complete)

    def test_invalid_meld_init(self):
        m = Meld()
        with self.assertRaises(InvalidMeldError):
            m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                     Card(rank=Rank.SIX, suit=Suit.CLUB))
        self.assertFalse(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)
        self.assertEqual(m.size(), 0) # failed init should have emptied meld

    def test_invalid_run_add(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.THREE, suit=Suit.HEART))
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)
        self.assertEqual(m.size(), 2)

        with self.assertRaises(InvalidMeldError):
            m.add(Card(rank=Rank.TWO, suit=Suit.CLUB))

        self.assertEqual(m.size(), 2)

    def test_invalid_set_add(self):
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)
        self.assertEqual(m.size(), 2)

        with self.assertRaises(InvalidMeldError):
            m.add(Card(rank=Rank.THREE, suit=Suit.CLUB))

        self.assertEqual(m.size(), 2)

    def test_invalid_add_does_not_break_complete_set(self):
        """A bad addition to a complete set doesn't break it."""
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.TWO, suit=Suit.CLUB),
                 Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertTrue(m.is_set)
        self.assertTrue(m.complete)

        with self.assertRaises(InvalidMeldError):
            m.add(Card(rank=Rank.THREE, suit=Suit.CLUB))

        self.assertEqual(m.size(), 3)
        self.assertTrue(m.all_same_rank)
        self.assertFalse(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertTrue(m.is_set)
        self.assertTrue(m.complete)

    def test_invalid_add_does_not_break_complete_run(self):
        """A bad addition to a complete run doesn't break it."""
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.THREE, suit=Suit.HEART),
                 Card(rank=Rank.FOUR, suit=Suit.HEART))
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.is_run)
        self.assertFalse(m.is_set)
        self.assertTrue(m.complete)

        with self.assertRaises(InvalidMeldError):
            m.add(Card(rank=Rank.SIX, suit=Suit.CLUB))

        self.assertEqual(m.size(), 3)
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.is_run)
        self.assertFalse(m.is_set)
        self.assertTrue(m.complete)

    def test_large_valid_run_grows_to_inside_straight(self):
        """A run becomes incomplete after inside straight conversion."""
        m = Meld(Card(rank=Rank.TWO, suit=Suit.HEART),
                 Card(rank=Rank.THREE, suit=Suit.HEART),
                 Card(rank=Rank.FOUR, suit=Suit.HEART))
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.is_run)
        self.assertFalse(m.is_set)
        self.assertTrue(m.complete)

        m.add(Card(rank=Rank.SIX, suit=Suit.HEART))

        self.assertEqual(m.size(), 4)
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.all_same_rank)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_singleton_add(self):
        """Test adding a card to a single-card partial meld.

        This is significant b/c until the 2nd card is added, any
        single-card partial meld is both a potential run and set.
        """
        m = Meld(Card(rank=Rank.KING, suit=Suit.CLUB))
        self.assertTrue(m.all_same_rank)
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

        m.add(Card(rank=Rank.TWO, suit=Suit.CLUB))
        self.assertFalse(m.all_same_rank)
        self.assertTrue(m.all_same_suit)
        self.assertFalse(m.is_run)
        self.assertFalse(m.is_set)
        self.assertFalse(m.complete)

    def test_remove_last(self):
        """Test removing the last card in a meld (leaving it empty)."""
        c = Card(rank=Rank.KING, suit=Suit.CLUB)
        m = Meld(c)
        m.remove(m.find(c))

if __name__ == '__main__':
    unittest.main()
