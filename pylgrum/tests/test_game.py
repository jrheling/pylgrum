import unittest
from unittest import skip
from pylgrum.game import Game
from pylgrum.player import Player

class TestGame(unittest.TestCase):

    def setUp(self):
        self.g = Game(Player(), Player())

    def test_game_init(self):
        self.assertEqual(self.g.player1.hand.size(), 10)
        self.assertEqual(self.g.player2.hand.size(), 10)
        self.assertEqual(self.g._discards.size(), 1)
        self.assertEqual(self.g._deck.size(), 31)

    def test_draw(self):
        self.assertEqual(self.g._deck.size(), 31)
        c1 = self.g._draw()
        self.assertEqual(self.g._deck.size(), 30)
        c2 = self.g._draw()
        self.assertFalse(c1.is_same_card(c2))

    def test_draw_discard(self):
        self.assertEqual(self.g._deck.size(), 31)
        self.assertEqual(self.g._discards.size(), 1)
        self.g._draw_discard()
        self.assertEqual(self.g._deck.size(), 31)
        self.assertEqual(self.g._discards.size(), 0)

    @skip("needs rest of turn lifecycle to work first?")
    def test_move_with_empty_discard_pile(self):
        # if the first move draws the discard, the discard pile will be empty
        self.g.start_new_move()
        self.g._draw_discard()
        self.g.acquire_card()
        self.g.start_new_move()

    def test_next_turn(self):
        self.assertEqual(self.g.player1, self.g._current_player)
        self.g.next_turn()
        self.assertEqual(self.g.player2, self.g._current_player)

    @skip("Cannot implement play test yet - need computer player.")
    def test_play(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
