"""
The service. Here will be the heart and soul of the game.
In this directory will be the min-max algorithm too

The service will have 2 main functions: player_vs_player and player_vs_computer

The human player will always move first
"""

from board.board import Board
from service.minmax import MinMax


class Connect4:

    def __init__(self, player1, player2, board):
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2
        self.__played_chips = 0
        self.__ai = MinMax()

    @property
    def played_chips(self):
        return self.__played_chips

    @property
    def player1_color(self):
        return self.__player1.color

    @property
    def player2_color(self):
        return self.__player2.color

    def play_player1(self, column):
        if not 1 <= column <= 7:
            raise ValueError('Column not between 1 and 7')

        column -= 1
        column = 6 - column
        row = self.__board.possible_row(column)

        if row == -1:
            raise ValueError('Column is full!')

        self.__board.add_chip(row, column, self.__player1)
        self.__played_chips += 1

    def play_player2(self, column):
        if not 1 <= column <= 7:
            raise ValueError('Column not between 1 and 7')

        column -= 1
        column = 6 - column
        row = self.__board.possible_row(column)

        if row == -1:
            raise ValueError('Column is full!')

        self.__played_chips += 1
        self.__board.add_chip(row, column, self.__player2)

    def check_win_player1(self):
        return self.__board.check_for_win(self.__player1)

    def check_win_player2(self):
        return self.__board.check_for_win(self.__player2)

    def play_ai(self):
        self.__ai.start_min_max_from(self.__board.mask, self.__played_chips + 1)
        new_mask = self.__ai.next_move
        column = self.__board.get_different_column(new_mask)
        row = self.__board.possible_row(column)

        if row == -1:
            raise ValueError('Column is full!')

        self.__board.add_chip(row, column, self.__player2)
        self.__played_chips += 1

    def get_board_console(self):
        return self.__board.get_board_console()

    def get_board(self):
        return self.__board.get_board()

    def clear(self):
        self.__board.clear()
        self.__played_chips = 0
