import unittest
from domain.position import Position
from domain.chip import Chip


class TestDomain(unittest.TestCase):

    def test_position(self):
        try:
            p = Position(-1, 2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        try:
            p = Position(1, -2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        try:
            p = Position(6, 2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        try:
            p = Position(2, 7)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        try:
            p = Position(23, 26)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        try:
            p = Position(-1, -2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        p = Position(0, 1)
        self.assertEqual(0, p.row)
        self.assertEqual(1, p.column)

    def test_chip(self):
        c = Chip('#FF0000', 'Computer')
        self.assertEqual('#FF0000', c.color)
        self.assertEqual('Computer', c.player)


def test_domain():
    if __name__ == '__main__':
        unittest.main()
