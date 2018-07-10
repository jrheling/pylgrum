import unittest
from unittest import skip
from context import Game, Player

class TestGame(unittest.TestCase):

    def setUp(self):
        self.g = Game(Player(), Player())

    def test_game_init(self):
        self.assertEqual(self.g.p1._hand.size(), 10)
        self.assertEqual(self.g.p2._hand.size(), 10)
        self.assertEqual(self.g._discards.size(), 1)
        self.assertEqual(self.g._deck.size(), 31)

    def test_draw(self):
        self.assertEqual(self.g._deck.size(), 31)
        c1 = self.g.draw()
        self.assertEqual(self.g._deck.size(), 30)
        c2 = self.g.draw()
        self.assertFalse(c1.is_same_card(c2))
        
    def test_draw_discard(self):
        self.assertEqual(self.g._deck.size(), 31)
        self.assertEqual(self.g._discards.size(), 1)
        c1 = self.g.draw_discard()
        self.assertEqual(self.g._deck.size(), 31)
        self.assertEqual(self.g._discards.size(), 0)

    @skip("Cannot implement play test yet - need computer player.")
    def test_play(self):
        self.assertTrue(False)
        
if __name__ == '__main__':
    unittest.main()
