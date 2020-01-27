import unittest
from pylgrum.card import Suit, Rank, Card

class TestCard(unittest.TestCase):

    def SetUp(self):
        pass

    def test_card_creation(self):
        c = Card(rank=Rank.QUEEN, suit=Suit.HEART)
        self.assertIsInstance(c.suit, Suit)
        self.assertIsInstance(c.rank, Rank)
        self.assertIs(c.suit, Suit.HEART)
        self.assertIs(c.rank, Rank.QUEEN)

    def test_royalty_scores_ten(self):
        j = Card(rank=Rank.JACK, suit=Suit.SPADE)
        k = Card(rank=Rank.KING, suit=Suit.DIAMOND)
        self.assertEqual(j.score_val(), 10)
        self.assertEqual(k.score_val(), 10)

    def test_comparisons(self):
        # suits are arbitrary here - this method is not testing suits
        three = Card(rank=Rank.THREE, suit=Suit.CLUB)
        otherthree = Card(rank=Rank.THREE, suit=Suit.SPADE)
        four = Card(rank=Rank.FOUR, suit=Suit.SPADE)
        self.assertTrue(three == otherthree)
        self.assertFalse(three == four)

        self.assertTrue(three != four)
        self.assertFalse(three != otherthree)

        self.assertTrue(three < four)
        self.assertFalse(three < otherthree)

        self.assertTrue(three <= four)
        self.assertFalse(four <= three)
        self.assertTrue(three <= otherthree)

        self.assertTrue(four > three)
        self.assertFalse(three > four)

        self.assertTrue(four >= three)
        self.assertFalse(three >= four)
        self.assertTrue(three >= otherthree)

    def test_ace_points(self):
        ace = Card(rank=Rank.ACE, suit=Suit.HEART)
        two = Card(rank=Rank.TWO, suit=Suit.SPADE)

        self.assertTrue(ace < two)

    def test_royal_points(self):
        nine = Card(rank=Rank.NINE, suit=Suit.CLUB)
        ten = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        jack = Card(rank=Rank.JACK, suit=Suit.HEART)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        self.assertEqual(ten, jack)
        self.assertFalse(jack < king)
        self.assertTrue(nine < jack)

    def test_same_suit(self):
        club1 = Card(rank=Rank.TWO, suit=Suit.CLUB)
        club2 = Card(rank=Rank.SEVEN, suit=Suit.CLUB)
        heart = Card(rank=Rank.FIVE, suit=Suit.HEART)

        self.assertTrue(club1.same_suit(club2))
        self.assertTrue(club2.same_suit(club1))
        self.assertFalse(club1.same_suit(heart))
        self.assertFalse(heart.same_suit(club1))

    def test_rank_val(self):
        nine = Card(rank=Rank.NINE, suit=Suit.CLUB)
        ten = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        jack = Card(rank=Rank.JACK, suit=Suit.HEART)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        self.assertEqual(nine.rank_val(), 9)
        self.assertEqual(ten.rank_val(), 10)
        self.assertEqual(jack.rank_val(), 11)
        self.assertEqual(king.rank_val(), 13)

    def test_sorted(self):
        nine = Card(rank=Rank.NINE, suit=Suit.CLUB)
        ten = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        jack = Card(rank=Rank.JACK, suit=Suit.HEART)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        cards = [king, ten, nine, jack]
        ascending = sorted(cards, key=lambda card: card.rank_val())
        expected = [nine, ten, jack, king]
        for i in range(0,len(cards)):
            self.assertTrue(ascending[i].is_same_card(expected[i]))

    def test_sort(self):
        nine = Card(rank=Rank.NINE, suit=Suit.CLUB)
        ten = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        jack = Card(rank=Rank.JACK, suit=Suit.HEART)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        cards = [king, ten, nine, jack]
        cards.sort(key=lambda card: card.rank_val())
        expected = [nine, ten, jack, king]
        for i in range(0,len(cards)):
            self.assertTrue(cards[i].is_same_card(expected[i]))

    def test_hash(self):
        three = Card(rank=Rank.THREE, suit=Suit.CLUB)
        otherthree = Card(rank=Rank.THREE, suit=Suit.CLUB)
        four = Card(rank=Rank.FOUR, suit=Suit.SPADE)

        self.assertEqual(hash(three), hash(otherthree))
        self.assertNotEqual(hash(three), hash(four))

        dict = {}
        dict[three] = "foo"
        self.assertEqual(dict[otherthree], "foo")

if __name__ == '__main__':
    unittest.main()
