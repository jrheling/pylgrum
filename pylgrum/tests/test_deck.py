import unittest
from pylgrum.card import Card, Rank, Suit
from pylgrum.deck import Deck

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.d = Deck()

    def test_deck_size(self):
        self.assertEqual(self.d.size(), 52)

    def test_deck_contents(self):
        """A deck should have one of each card."""
        for c in [Card(rank=r, suit=s)
                  for r in list(Rank)
                  for s in list(Suit)]:
            self.d.find(c)

if __name__ == '__main__':
    unittest.main()
