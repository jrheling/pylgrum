import unittest
from unittest import skip
from pylgrum.tui.tui_player import TUIPlayer

class TestTUIPlayer(unittest.TestCase):

    def setUp(self):
        self.p1 = TUIPlayer('p1')

    def test_normalize_input(self):
        f = self.p1.normalize_input
        self.assertEqual(f('c'),'c')
        self.assertEqual(f('1'),1)
        self.assertEqual(f('D'),'D')
        self.assertEqual(f('42'),42)
        self.assertEqual(f('word with spaces'),'word with spaces')
        self.assertEqual(f('-24'),-24)

if __name__ == '__main__':
    unittest.main()
