import unittest
from pylgrum.card import Card, Rank, Suit
from pylgrum.stack import CardStack
from pylgrum.errors import CardNotFoundError

def get_test_stack() -> CardStack:
    """Returns stack of 12 cards for reference by test cases."""

    cs = CardStack()
    # Note: tests below depend on the details of this deck
    cs.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))    # 0 : QH
    cs.add(Card(rank=Rank.JACK, suit=Suit.DIAMOND))   # 1 : JD
    cs.add(Card(rank=Rank.ACE, suit=Suit.CLUB))       # 2 : AC
    cs.add(Card(rank=Rank.KING, suit=Suit.SPADE))     # 3 : KS
    cs.add(Card(rank=Rank.TWO, suit=Suit.HEART))      # 4 : 2H
    cs.add(Card(rank=Rank.THREE, suit=Suit.DIAMOND))  # 5 : 3D
    cs.add(Card(rank=Rank.FOUR, suit=Suit.CLUB))      # 6 : 4C
    cs.add(Card(rank=Rank.FIVE, suit=Suit.SPADE))     # 7 : 5S
    cs.add(Card(rank=Rank.TEN, suit=Suit.HEART))      # 8 : 10H
    cs.add(Card(rank=Rank.NINE, suit=Suit.DIAMOND))   # 9 : 9D
    cs.add(Card(rank=Rank.EIGHT, suit=Suit.CLUB))     # 10: 8C
    cs.add(Card(rank=Rank.SEVEN, suit=Suit.SPADE))    # 11: 7S

    return cs

class TestStack(unittest.TestCase):

    def SetUp(self):
        pass

    def test_stack_add(self):
        cs = CardStack()
        c = Card(rank=Rank.QUEEN, suit=Suit.HEART)

        self.assertEqual(cs.size(), 0)
        cs.add(c)
        self.assertEqual(cs.size(), 1)

    def test_stack_remove(self):
        cs = get_test_stack()
        two_h = Card(rank=Rank.TWO, suit=Suit.HEART)
        three_d = Card(rank=Rank.THREE, suit=Suit.DIAMOND)

        self.assertEqual(cs.size(), 12)
        removed_card = cs.remove(4)
        self.assertEqual(removed_card,two_h)

        self.assertEqual(cs.size(), 11)
        removed_card = cs.remove(4)
        self.assertEqual(removed_card,three_d)
        self.assertEqual(cs.size(), 10)

    def test_stack_remove_last(self):
        cs = CardStack()
        c = Card(rank=Rank.QUEEN, suit=Suit.HEART)

        self.assertEqual(cs.size(), 0)
        cs.add(c)
        self.assertEqual(cs.size(), 1)
        cs.remove(cs.find(c))
        self.assertEqual(cs.size(), 0)

    def test_stack_get(self):
        cs = get_test_stack()
        two_h = Card(rank=Rank.TWO, suit=Suit.HEART)
        three_d = Card(rank=Rank.THREE, suit=Suit.DIAMOND)

        self.assertEqual(cs.size(), 12)
        self.assertEqual(cs.get(4),two_h)

        self.assertEqual(cs.size(), 12)
        self.assertEqual(cs.get(5),three_d)
        self.assertEqual(cs.size(), 12)

    def test_stack_remove_miss(self):
        cs = get_test_stack()

        with self.assertRaises(CardNotFoundError):
            cs.remove(24) # index out of bounds

    def test_stack_find(self):
        cs = get_test_stack()
        three_diamond = Card(rank=Rank.THREE, suit=Suit.DIAMOND)

        pos = cs.find(three_diamond)
        self.assertEqual(pos, 5)

    def test_stack_find_miss(self):
        cs = get_test_stack()
        qd = Card(rank=Rank.QUEEN, suit=Suit.DIAMOND) # card not in stack

        with self.assertRaises(CardNotFoundError):
            cs.find(qd)

    def test_stack_draw(self):
        cs = get_test_stack()

        self.assertEqual(cs.size(), 12)
        seven_spade = cs.draw()
        self.assertTrue(seven_spade.is_same_card(Card(rank=Rank.SEVEN,
                                                      suit=Suit.SPADE)))

        self.assertEqual(cs.size(), 11)

    def test_stack_peek_sees_top(self):
        cs = get_test_stack()

        self.assertEqual(cs.size(), 12)
        seven_spade = cs.peek()
        self.assertTrue(seven_spade.is_same_card(Card(rank=Rank.SEVEN,
                                                      suit=Suit.SPADE)))

        self.assertEqual(cs.size(), 12)

    def test_stack_shuffle(self):
        cs1 = get_test_stack()
        cs2 = get_test_stack()

        self.assertTrue(cs1 == cs2)
        cs1.shuffle()
        self.assertFalse(cs1 == cs2) # false negative unlikely but possible

    def test_stack_eq(self):
        cs1 = get_test_stack()
        cs2 = get_test_stack()

        self.assertTrue(cs1 == cs2)
        cs2.remove(2)
        self.assertFalse(cs1 == cs2)

    def test_peek_empty_stack(self):
        cs = CardStack()
        with self.assertRaises(CardNotFoundError):
            cs.peek()

    def test_draw_empty_stack(self):
        cs = CardStack()
        with self.assertRaises(CardNotFoundError):
            cs.draw()

if __name__ == '__main__':
    unittest.main()
