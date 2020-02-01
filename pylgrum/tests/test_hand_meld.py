import unittest
from unittest import skip
from pylgrum.card import Card, Rank, Suit
from pylgrum.meld import Meld
from pylgrum.hand_melds import HandWithMelds
from pylgrum.errors import InvalidMeldError

class TestHandWithMelds(unittest.TestCase):

    def setUp(self):
        self.h = HandWithMelds()

        self.h.add(Card(rank=Rank.QUEEN, suit=Suit.HEART))    # 0 : QH
        self.h.add(Card(rank=Rank.JACK, suit=Suit.DIAMOND))   # 1 : JD
        self.h.add(Card(rank=Rank.ACE, suit=Suit.CLUB))       # 2 : AC
        self.h.add(Card(rank=Rank.KING, suit=Suit.SPADE))     # 3 : KS
        self.h.add(Card(rank=Rank.TWO, suit=Suit.HEART))      # 4 : 2H
        self.h.add(Card(rank=Rank.THREE, suit=Suit.DIAMOND))  # 5 : 3D
        self.h.add(Card(rank=Rank.FOUR, suit=Suit.CLUB))      # 6 : 4C
        self.h.add(Card(rank=Rank.FIVE, suit=Suit.SPADE))     # 7 : 5S
        self.h.add(Card(rank=Rank.TEN, suit=Suit.HEART))      # 8 : 10H
        self.h.add(Card(rank=Rank.NINE, suit=Suit.DIAMOND))   # 9 : 9D
        self.h.add(Card(rank=Rank.EIGHT, suit=Suit.CLUB))     # 10: 8C

    def test_empty_meld_creation(self):
        self.assertEqual(len(self.h._melds), 0)
        self.h.create_meld()
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 0)

    def test_nonempty_meld_creation(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d, three_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])

    def test_invalid_meld_creation(self):
        jack_d = self.h.cards[1]
        two_h = self.h.cards[4]
        with self.assertRaises(InvalidMeldError):
            self.h.create_meld(jack_d, two_h)
        self.assertEqual(len(self.h._melds), 0)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 0)

    def test_singleton_meld_creation(self):
        two_h = self.h.cards[4]
        self.h.create_meld(two_h)
        self.assertEqual(len(self.h._melds), 1)

    def test_card_add(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 1)
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[jack_d])

        self.h.add_to_meld(self.h._melds[0], three_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[three_d])

    def test_card_add_by_idx(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 1)
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[jack_d])

        self.h.add_to_meld_by_idx(0,5)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[three_d])

    def test_card_add_invalid(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        two_h = self.h.cards[4]
        self.h.create_meld(jack_d, three_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[jack_d])
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[three_d])

        with self.assertRaises(InvalidMeldError):
            self.h.add_to_meld(self.h._melds[0], two_h)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[jack_d])
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[three_d])

    def test_card_in_n_melds(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d, three_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        self.assertEqual(len(self.h._card_to_meld_id[jack_d]), 1)

        # add one card to a second meld
        self.h.create_meld(jack_d)
        self.assertEqual(len(self.h._melds), 2)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        self.assertTrue(id(self.h._melds[1]) in self.h._card_to_meld_id[jack_d])
        self.assertEqual(len(self.h._card_to_meld_id[jack_d]), 2)

        # and remove it
        self.h.remove_from_meld(self.h._melds[1], jack_d)
        self.assertEqual(len(self.h._melds), 2)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        self.assertFalse(id(self.h._melds[1]) in
                         self.h._card_to_meld_id[jack_d])
        self.assertEqual(len(self.h._card_to_meld_id[jack_d]), 1)

    def test_melds_with_overused_cards(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        m1 = self.h.create_meld(jack_d, three_d)
        m2 = self.h.create_meld(jack_d)
        m3 = self.h.create_meld(self.h.cards[4])
        overused = self.h.melds_with_overused_cards()
        self.assertIn(m1, overused)
        self.assertIn(m2, overused)
        self.assertNotIn(m3, overused)

    def test_melds_using_card(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d, three_d)
        self.h.create_meld(jack_d)
        self.h.create_meld(three_d)

        melds_using_jack = self.h.melds_using_card(jack_d)
        self.assertTrue(self.h._melds[0] in melds_using_jack)
        self.assertTrue(self.h._melds[1] in melds_using_jack)
        self.assertFalse(self.h._melds[2] in melds_using_jack)

    def test_card_remove(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d, three_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        self.assertTrue(id(self.h._melds[0]) in
                        self.h._card_to_meld_id[three_d])

        self.h.remove_from_meld(self.h._melds[0], three_d)

        self.assertEqual(len(self.h._card_to_meld_id.keys()), 1)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        with self.assertRaises(KeyError):
            self.h._card_to_meld_id[three_d]

    def test_meld_remove_empty(self):
        self.assertEqual(len(self.h._melds), 0)
        self.h.create_meld()
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 0)

        self.h.remove_meld(self.h._melds[0])
        self.assertEqual(len(self.h._melds), 0)

    def test_meld_remove_nonempty(self):
        jack_d = self.h.cards[1]
        three_d = self.h.cards[5]
        self.h.create_meld(jack_d, three_d)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        self.assertEqual(len(self.h._card_to_meld_id[jack_d]), 1)

        # add one card to a second meld
        self.h.create_meld(jack_d)
        self.assertEqual(len(self.h._melds), 2)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 2)
        self.assertTrue(id(self.h._melds[0]) in self.h._card_to_meld_id[jack_d])
        self.assertTrue(id(self.h._melds[1]) in self.h._card_to_meld_id[jack_d])
        self.assertEqual(len(self.h._card_to_meld_id[jack_d]), 2)

        # remove the first meld
        removed_meld = self.h._melds[0]
        retained_meld = self.h._melds[1]
        self.h.remove_meld(removed_meld)
        self.assertEqual(len(self.h._melds), 1)
        self.assertEqual(len(self.h._card_to_meld_id.keys()), 1)
        self.assertTrue(id(retained_meld) in self.h._card_to_meld_id[jack_d])
        self.assertFalse(id(removed_meld) in self.h._card_to_meld_id[jack_d])
        self.assertEqual(len(self.h._card_to_meld_id[jack_d]), 1)
        with self.assertRaises(KeyError):
            self.h._card_to_meld_id[three_d]

    def test_hand_with_no_melds_is_valid(self):
        hm = HandWithMelds()
        self.assertTrue(hm.is_valid)

    def test_hand_with_no_overused_cards_is_valid(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd) = Card.from_text("QH", "QD", "QC", "KD")
        hm.add([qh, qd, qc, kd])
        hm.create_meld(qh, qd, qc)
        hm.create_meld(kd)
        self.assertTrue(hm.is_valid)

    def test_hand_with_overused_cards_is_valid_if_only_one_is_complete(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd, jd, jh, js) = Card.from_text("QH", "QD", "QC", "KD", "JD", "JH", "JS")
        hm.add([qh, qd, qc, kd, jd, jh, js])
        hm.create_meld(qh, qd, qc)     # qd overlaps between this
        hm.create_meld(kd, qd)         #   and this, but only the first is complete
        hm.create_meld(jd, jh, js)     # no overlap on this one
        self.assertTrue(hm.is_valid)

    def test_hand_with_overused_cards_is_invalid(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd, jd, jh) = Card.from_text("QH", "QD", "QC", "KD", "JD", "JH")
        hm.add([qh, qd, qc, kd, jd, jh])
        hm.create_meld(qh, qd, qc)     # qd overlaps between this
        hm.create_meld(kd, qd, jd)         #   and this
        hm.create_meld(jd, jh)         # overlap here, but incomplete
        self.assertFalse(hm.is_valid)

    def test_is_deadwood_is_true_for_cards_not_in_any_meld(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd, threec) = Card.from_text("QH", "QD", "QC", "KD", "3C")
        cards = [qh, qd, qc, kd, threec]
        hm.add(cards)
        hm.create_meld(qh, qd, qc)
        expected_deadwood = [False, False, False, True, True]
        for idx, card in enumerate(cards):
            self.assertEqual(hm.is_deadwood(card), expected_deadwood[idx])

    def test_is_deadwood_is_true_for_cards_in_incomplete_meld(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd, threec) = Card.from_text("QH", "QD", "QC", "KD", "3C")
        cards = [qh, qd, qc, kd, threec]
        hm.add(cards)
        hm.create_meld(qh, qd, qc)
        hm.create_meld(threec)
        expected_deadwood = [False, False, False, True, True]
        for idx, card in enumerate(cards):
            self.assertEqual(hm.is_deadwood(card), expected_deadwood[idx])

    def test_deadwood_returns_cards_not_in_complete_meld(self):
        # this test covers deadwood in no melds and deadwood in incomplete meld
        hm = HandWithMelds()
        (qh, qd, qc, kd, threec) = Card.from_text("QH", "QD", "QC", "KD", "3C")
        cards = [qh, qd, qc, kd, threec]
        hm.add(cards)
        hm.create_meld(qh, qd, qc)
        hm.create_meld(threec)
        expected_deadwood = [threec, kd]
        for card in expected_deadwood:
            self.assertTrue(card in hm.deadwood())

    def test_deadwood_count_includes_cards_not_in_complete_melds(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd) = Card.from_text("QH", "QD", "QC", "KD")
        hm.add([qh, qd, qc, kd])
        hm.create_meld(qh, qd, qc)
        hm.create_meld(kd)
        self.assertEqual(hm.deadwood_count, 1)

    def test_deadwood_value_sums_points_of_cards_not_in_complete_melds(self):
        hm = HandWithMelds()
        (qh, qd, qc, kd, threec) = Card.from_text("QH", "QD", "QC", "KD", "3C")
        hm.add([qh, qd, qc, kd, threec])
        hm.create_meld(qh, qd, qc)
        hm.create_meld(threec)
        # the three and the kd are both deadwood here
        self.assertEqual(hm.deadwood_value, 13)

if __name__ == '__main__':
    unittest.main()
