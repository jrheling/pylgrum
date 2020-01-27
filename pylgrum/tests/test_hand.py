import unittest
from pylgrum.card import Card, Rank, Suit
from pylgrum.hand import Hand
from pylgrum.errors import OverdealtHandError

class TestHand(unittest.TestCase):

    def test_too_many_cards(self):
        """Implicitly tests the add() override in Hand, too."""
        h = Hand()
        self.assertEqual(h.size(), 0)

        h.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))    # 0 : QH
        h.add(Card(rank=Rank.JACK, suit=Suit.DIAMOND))   # 1 : JD
        h.add(Card(rank=Rank.ACE, suit=Suit.CLUB))       # 2 : AC
        h.add(Card(rank=Rank.KING, suit=Suit.SPADE))     # 3 : KS
        h.add(Card(rank=Rank.TWO, suit=Suit.HEART))      # 4 : 2H
        h.add(Card(rank=Rank.THREE, suit=Suit.DIAMOND))  # 5 : 3D
        h.add(Card(rank=Rank.FOUR, suit=Suit.CLUB))      # 6 : 4C
        h.add(Card(rank=Rank.FIVE, suit=Suit.SPADE))     # 7 : 5S
        h.add(Card(rank=Rank.TEN, suit=Suit.HEART))      # 8 : 10H
        h.add(Card(rank=Rank.NINE, suit=Suit.DIAMOND))   # 9 : 9D
        h.add(Card(rank=Rank.EIGHT, suit=Suit.CLUB))     # 10: 8C
        self.assertEqual(h.size(), 11) ## a full hand

        with self.assertRaises(OverdealtHandError):
            h.add(Card(rank=Rank.SEVEN, suit=Suit.SPADE))


if __name__ == '__main__':
    unittest.main()
