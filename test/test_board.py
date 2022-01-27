"""
Test unit for the board elements: Mask and board
"""


import unittest
from board.board import *
from domain.chip import Chip


class TestBoard(unittest.TestCase):

    def test_mask(self):
        mask = Mask()
        mask.drop_chip(0, 0, 1)
        self.assertEqual(mask.mask, 1)
        mask.mask = 7
        self.assertFalse(mask.check_if_move_possible(0, 1))
        self.assertEqual(mask.simulate_chip_drop(0, 2, 1), 16)
        self.assertFalse(mask.check_mask_for_win(1))
        self.assertEqual(mask.approximate_points(1), 3)
        self.assertEqual(mask.approximate_points(2), 3)

    def test_board(self):
        player1 = Chip('Red', 'HumanPlayer1')
        player2 = Chip('Yellow', 'HumanPlayer2')
        board = Board(player1, player2)
        board.board_to_mask()
        self.assertEqual(board.mask, 0)
        board.add_chip(0, 3, player1)
        board.add_chip(1, 3, player2)
        board.board_to_mask()
        self.assertEqual(board.mask, 118125)
        board.mask = 7
        board.mask_to_board()

        board2 = Board(player1, player2)
        board2.add_chip(0, 0, player1)
        board2.add_chip(0, 1, player2)

        self.assertTrue(board.__eq__(board2))

        self.assertEqual(board.piece_to_nr(player1), 1)
        self.assertEqual(board.piece_to_nr(player2), 2)

        board2.add_chip(1, 0, player1)
        board2.add_chip(1, 1, player2)
        board2.add_chip(2, 0, player1)
        board2.add_chip(2, 1, player2)
        board2.add_chip(3, 0, player1)

        self.assertTrue(board2.check_for_win(player1))
        self.assertFalse(board2.check_for_win(player2))

        self.assertEqual(board.possible_row(0), 1)
        self.assertEqual(board.possible_row(3), 0)

        board.clear()
        self.assertEqual(board.mask, 0)

        self.assertEqual(board.get_different_column(1), 0)


if __name__ == '__main__':
    unittest.main()
