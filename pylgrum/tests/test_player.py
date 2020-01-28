import unittest
from pylgrum.player import Player
from pylgrum.card import Card, Suit, Rank
from pylgrum.errors import OverdealtHandError, PylgrumInternalError
from pylgrum.tui.hand_melds import HandWithMelds

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.p = Player()

    def test_initial_hand_size(self):
        self.assertEqual(self.p.hand.size(), 0)

    def test_receive_card(self):
        self.p.receive_card(Card(rank=Rank.TEN, suit=Suit.HEART))
        self.assertEqual(self.p.hand.size(), 1)

    def test_too_many_cards(self):
        self.p.receive_card(Card(rank=Rank.QUEEN, suit=Suit.HEART))    # 0 : QH
        self.p.receive_card(Card(rank=Rank.JACK, suit=Suit.DIAMOND))   # 1 : JD
        self.p.receive_card(Card(rank=Rank.ACE, suit=Suit.CLUB))       # 2 : AC
        self.p.receive_card(Card(rank=Rank.KING, suit=Suit.SPADE))     # 3 : KS
        self.p.receive_card(Card(rank=Rank.TWO, suit=Suit.HEART))      # 4 : 2H
        self.p.receive_card(Card(rank=Rank.THREE, suit=Suit.DIAMOND))  # 5 : 3D
        self.p.receive_card(Card(rank=Rank.FOUR, suit=Suit.CLUB))      # 6 : 4C
        self.p.receive_card(Card(rank=Rank.FIVE, suit=Suit.SPADE))     # 7 : 5S
        self.p.receive_card(Card(rank=Rank.TEN, suit=Suit.HEART))      # 8 : 10H
        self.p.receive_card(Card(rank=Rank.NINE, suit=Suit.DIAMOND))   # 9 : 9D
        self.p.receive_card(Card(rank=Rank.EIGHT, suit=Suit.CLUB))     # 10: 8C
        self.assertEqual(self.p.hand.size(), 11) ## a full hand

        with self.assertRaises(OverdealtHandError):
            self.p.receive_card(Card(rank=Rank.SEVEN, suit=Suit.SPADE))

    def test_bad_handtype(self):
        with self.assertRaises(PylgrumInternalError):
            player = Player(handtype=object) # pylint: disable=unused-variable

    def test_nondefault_handtype(self):
        """Test instantiation of Player with a non-default hand type.

        Note: testing alternate hand types is done elsewhere - here we just
        want to make sure the Player can be instantiated.
        """
        player = Player(HandWithMelds)
        self.assertIsInstance(player, Player)

    def test_contestant_id(self):
        player = Player(contestant_id='foo bar baz')
        self.assertEqual(player.contestant_id, "foo bar baz")

if __name__ == '__main__':
    unittest.main()
