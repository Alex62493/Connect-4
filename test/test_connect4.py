from service.connect4 import Connect4
from domain.chip import Chip
from board.board import Board
import unittest


class TestService(unittest.TestCase):

    def test_connect4(self):
        player1 = Chip('Red', 'Player1')
        player2 = Chip('Yellow', 'Player2')
        board = Board(player1, player2)
        serv = Connect4(player1, player2, board)

        self.assertEqual(serv.played_chips, 0)

        try:
            serv.play_player1(8)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        try:
            serv.play_player2(0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        serv.play_player1(1)
        serv.play_player2(1)
        serv.play_player2(1)
        serv.play_player2(1)
        serv.play_player2(1)

        self.assertFalse(serv.check_win_player1())
        self.assertTrue(serv.check_win_player2())
        self.assertEqual(serv.played_chips, 5)

        print(serv.get_board_console())
