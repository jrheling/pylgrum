import unittest
from pylgrum.card import Suit, Rank, Card

class TestCard(unittest.TestCase):

    def SetUp(self):
        pass

    def test_card_creation_with_init(self):
        c = Card(rank=Rank.QUEEN, suit=Suit.HEART)
        self.assertIsInstance(c.suit, Suit)
        self.assertIsInstance(c.rank, Rank)
        self.assertIs(c.suit, Suit.HEART)
        self.assertIs(c.rank, Rank.QUEEN)

    def test_face_card_creation_from_text(self):
        c = Card.from_text("QH")
        self.assertIsInstance(c.suit, Suit)
        self.assertIsInstance(c.rank, Rank)
        self.assertIs(c.suit, Suit.HEART)
        self.assertIs(c.rank, Rank.QUEEN)

    def test_nonface_card_creation_from_text(self):
        c = Card.from_text("3C")
        self.assertIsInstance(c.suit, Suit)
        self.assertIsInstance(c.rank, Rank)
        self.assertIs(c.suit, Suit.CLUB)
        self.assertIs(c.rank, Rank.THREE)

    def test_multiple_card_creation_from_text(self):
        cards = Card.from_text("3C","4S","QH")
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0], Card.from_text("3C"))
        self.assertEqual(cards[2], Card.from_text("QH"))

    def test_royalty_scores_ten(self):
        j = Card(rank=Rank.JACK, suit=Suit.SPADE)
        k = Card(rank=Rank.KING, suit=Suit.DIAMOND)
        self.assertEqual(j.score_val(), 10)
        self.assertEqual(k.score_val(), 10)

    def test_comparisons(self):
        # where suits are compared, Spade > Heart > Club > Diamond
        three_c = Card(rank=Rank.THREE, suit=Suit.CLUB)
        three_s = Card(rank=Rank.THREE, suit=Suit.SPADE)
        four_s = Card(rank=Rank.FOUR, suit=Suit.SPADE)
        two_s = Card(rank=Rank.TWO, suit=Suit.SPADE)

        three_c2 = Card(rank=Rank.THREE, suit=Suit.CLUB)

        self.assertTrue(three_c == three_c2)
        self.assertFalse(three_c == three_s)
        self.assertFalse(three_c == four_s)

        self.assertTrue(three_s > three_c)
        self.assertFalse(three_c == three_s)

        self.assertTrue(three_c < four_s)
        self.assertTrue(three_c < three_s)

        self.assertTrue(three_c < two_s)       # suit is more important than rank
        self.assertFalse(four_s <= three_c)

        self.assertTrue(four_s >= three_c)
        self.assertFalse(three_c >= four_s)
        self.assertTrue(three_c < three_s)

    def test_same_score_different_sorting(self):
        jack = Card(rank=Rank.JACK, suit=Suit.SPADE)
        ten = Card(rank=Rank.TEN, suit=Suit.SPADE)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        self.assertTrue(jack.score_val() == ten.score_val())
        self.assertTrue(king.score_val() == ten.score_val())

        self.assertFalse(jack == ten)
        self.assertFalse(jack == king)
        self.assertFalse(king == ten)

    def test_ace_points(self):
        ace = Card(rank=Rank.ACE, suit=Suit.HEART)
        two = Card(rank=Rank.TWO, suit=Suit.SPADE)

        self.assertTrue(ace.score_val() < two.score_val())

    def test_royal_points(self):
        nine = Card(rank=Rank.NINE, suit=Suit.CLUB)
        ten = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        jack = Card(rank=Rank.JACK, suit=Suit.HEART)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        self.assertEqual(ten.score_val(), jack.score_val())
        self.assertFalse(jack.score_val() < king.score_val())
        self.assertTrue(nine.score_val() < jack.score_val())

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

    def test_card_sort_by_rank(self):
        nine = Card(rank=Rank.NINE, suit=Suit.CLUB)
        ten = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        jack = Card(rank=Rank.JACK, suit=Suit.HEART)
        king = Card(rank=Rank.KING, suit=Suit.SPADE)

        cards = [king, ten, nine, jack]
        cards.sort(key=lambda card: card.rank.value)
        expected = [nine, ten, jack, king]
        for i in range(0,len(cards)):
            self.assertTrue(cards[i].is_same_card(expected[i]))

    def test_card_sort_by_suit(self):
        # expected order Spade > Heart > Club > Diamond
        club = Card(rank=Rank.NINE, suit=Suit.CLUB)
        diamond = Card(rank=Rank.TEN, suit=Suit.DIAMOND)
        heart = Card(rank=Rank.JACK, suit=Suit.HEART)
        spade = Card(rank=Rank.KING, suit=Suit.SPADE)

        cards = [club, heart, diamond, spade]
        cards.sort(key=lambda card: card.suit.value)
        expected = [diamond, club, heart, spade]
        for i in range(0,len(cards)):
            print("expect {} to match {}".format(cards[i], expected[i]))
            self.assertTrue(cards[i].is_same_card(expected[i]))

if __name__ == '__main__':
    unittest.main()
