import unittest
from context import Suit, Rank, Card

class TestCard(unittest.TestCase):

    def SetUp(self):
        pass

    def test_royalty_scores_ten(self):
        j = Card(Suit.SPADE, Rank.JACK)
        k = Card(Suit.DIAMOND, Rank.KING)
        # j = pylgrum.Card(pylgrum.Suit.SPADE, pylgrum.Rank.JACK)
        # k = pylgrum.Card(pylgrum.Suit.DIAMOND, pylgrum.Rank.KING)        
        self.assertEqual(j.score_val(), 10)
        self.assertEqual(k.score_val(), 10)


if __name__ == '__main__':
    unittest.main()
