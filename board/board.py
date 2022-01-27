"""
The playing board is defined here
The board has 6 rows and 7 columns, so the max nr of moves is 42

At the moment the idea is to have a table that shows which chips are where, and some kind of mask to show which slots
are occupied

So, with that in mind, the mask will be between 0 (no pieces) and 2^43-1 (full), each 1 in the binary representation
being a piece

x - empty
r - red pieces
y - yellow pieces

xxxxxxx
xxxxxxx
xxxxxxx
xxxxxxx
xxyxyxx
xxryrrr

The board above is 101000011111 in binary, so the mak will be 2591
Depending on my implementation later on, the mask may also be represented in base 3, so it will be 21000012111, 137929
in decimal. A little bit more space consuming, but also a lot clearer for a minmax implementation (I think)
Either way, the board will have: board - an 6x7 array filled with chips and 0 for the unoccupied spaces
                                 mask - an number in base 2 or base 3, which will represent it a little bit more space
                                        efficient than a board. I need this for the AI (I think). I mean, I can search
                                        the current board in the minmax tree with this max, and i can translate a board
                                        to a mask and vice-versa.
                                        After some thought, it will be a class on its own.
                                        Update: It will be in base 3, I hope

By the way, the board is inverted:

row / column 6 5 4 3 2 1 0
5            X X X X X X X
4            X X X X X X X
3            X X X X X X X
2            X X X X X X X
1            X X X X X X X
0            X X X X X X X

[0][0] is not top-left, it is bottom-right. It has a lot more sense regarding the mask
"""

from domain.chip import Chip
import random


class BoardError(Exception):

    def __init__(self, msg):
        self.__msg = msg


class Mask:

    def __init__(self, mask=0):
        self.__mask = mask

    @property
    def mask(self):
        return self.__mask

    @mask.setter
    def mask(self, mask):
        self.__mask = mask

    @property
    def rows(self):
        return 6

    @property
    def columns(self):
        return 7

    def drop_chip(self, row, column, nr):
        if not self.check_if_move_possible(row, column):
            raise BoardError("The position is already occupied!")

        pos_on_board = row*7 + column
        self.__mask += nr*(3 ** pos_on_board)

    def check_if_move_possible(self, row, column):
        pos_on_board = row * 7 + column
        copy = self.__mask
        copy //= 3 ** pos_on_board
        if copy % 3 == 0:
            return True
        else:
            return False

    def simulate_chip_drop(self, row, column, nr):
        pos_on_board = row * 7 + column
        mask = self.__mask + nr * (3 ** pos_on_board)
        return mask

    def create_board_from_mask(self):
        board = []
        mask = self.__mask
        i = -1
        for row in range(self.rows):
            board.append([])
            i += 1
            for column in range(self.columns):
                board[i].append(mask % 3)
                mask //= 3

        return board

    def check_mask_for_win(self, nr):
        board = self.create_board_from_mask()


        x_axis = [-1, -1, 0, 1, 1, 1, 0, -1]
        y_axis = [0, -1, -1, -1, 0, 1, 1, 1]

        for row in range(self.rows):
            for column in range(self.columns):
                for i in range(4):
                    if board[row][column] == nr:
                        x = column
                        y = row
                        nr_of_pieces = 0

                        while 0 <= x < self.columns and 0 <= y < self.rows and board[y][x] == nr:
                            nr_of_pieces += 1
                            x += x_axis[i]
                            y += y_axis[i]

                        j = i + 4
                        x = column + x_axis[j]
                        y = row + y_axis[j]

                        while 0 <= x < self.columns and 0 <= y < self.rows and board[y][x] == nr:
                            nr_of_pieces += 1
                            x += x_axis[j]
                            y += y_axis[j]

                        if nr_of_pieces >= 4:
                            return True

                for i in range(4, 8):
                    if board[row][column] == nr:
                        x = column
                        y = row
                        nr_of_pieces = 0

                        while 0 <= x < self.columns and 0 <= y < self.rows and board[y][x] == nr:
                            nr_of_pieces += 1
                            x += x_axis[i]
                            y += y_axis[i]

                        if nr_of_pieces >= 4:
                            return True

        return False

    def get_random_colon_list(self):
        columns = []

        for i in range(self.columns):
            nr = random.randrange(self.columns)
            while nr in columns:
                nr = random.randrange(self.columns)
            columns.append(nr)

        return columns

    def approximate_points(self, nr):
        board = self.create_board_from_mask()
        minimum = 100

        x_axis = [1, 1, 0, -1]
        y_axis = [0, 1, 1, 1]

        for row in range(self.rows):
            for column in range(self.columns):
                for i in range(4):
                    if board[row][column] == nr:
                        x = column
                        y = row
                        nr_of_pieces = 0

                        while 0 <= x < self.columns and 0 <= y < self.rows and board[y][x] == nr:
                            nr_of_pieces += 1
                            x += x_axis[i]
                            y += y_axis[i]

                        x1 = x
                        y1 = y

                        to_complete = 4 - nr_of_pieces

                        while 0 <= x < self.columns and 0 <= y < self.rows and board[y][x] == 0 and nr_of_pieces < 4:
                            nr_of_pieces += 1
                            x += x_axis[i]
                            y += y_axis[i]

                        if nr_of_pieces == 4:
                            if i == 2:
                                minimum = min(minimum, to_complete)
                            else:
                                needed_pieces = 0
                                x = x1
                                y = y1

                                for j in range(to_complete):
                                    for complete_row in range(y, -1, -1):
                                        if board[complete_row][x] != 0:
                                            break
                                        else:
                                            needed_pieces += 1
                                    x += x_axis[i]
                                    y += y_axis[i]

                                minimum = min(minimum, needed_pieces)

        return minimum


class Board(Mask):

    def __init__(self, piece1, piece2, mask=0):
        super(Board, self).__init__(mask)
        self.__player1 = piece1
        self.__player2 = piece2
        self.__board = []
        self.mask_to_board()

    def mask_to_board(self):
        self.__board = []
        for row in range(0, self.rows):
            self.__board.append([])
            for column in range(0, self.columns):
                self.__board[row].append(0)

        mask_copy = self.mask

        for row in range(self.rows):
            for column in range(self.columns):
                piece = mask_copy % 3
                if piece == 1:
                    self.__board[row][column] = self.__player1
                elif piece == 2:
                    self.__board[row][column] = self.__player2
                mask_copy //= 3

    def board_to_mask(self):
        self.mask = 0
        power = 0

        for row in range(self.rows):
            for column in range(self.columns):
                if self.__board[row][column] == self.__player1:
                    self.mask += 1 * (3 ** power)
                elif self.__board[row][column] == self.__player2:
                    self.mask += 2 * (3 ** power)
                power += 1

    def piece_to_nr(self, piece):
        if piece == self.__player1:
            return 1
        else:
            return 2

    def add_chip(self, row, column, piece):
        self.drop_chip(row, column, self.piece_to_nr(piece))
        self.__board[row][column] = piece

    def possible_row(self, column):
        for row in range(self.rows):
            if self.__board[row][column] == 0:
                return row

        return -1

    def check_for_win(self, player):
        x_axis = [-1, -1, 0, 1, 1, 1, 0, -1]
        y_axis = [0, -1, -1, -1, 0, 1, 1, 1]

        for row in range(self.rows):
            for column in range(self.columns):
                for i in range(4):
                    if self.__board[row][column] == player:
                        x = column
                        y = row
                        nr_of_pieces = 0

                        while 0 <= x < self.columns and 0 <= y < self.rows and self.__board[y][x] == player:
                            nr_of_pieces += 1
                            x += x_axis[i]
                            y += y_axis[i]

                        j = i + 4
                        x = column + x_axis[j]
                        y = row + y_axis[j]

                        while 0 <= x < self.columns and 0 <= y < self.rows and self.__board[y][x] == player:
                            nr_of_pieces += 1
                            x += x_axis[j]
                            y += y_axis[j]

                        if nr_of_pieces >= 4:
                            return True

                for i in range(4, 8):
                    if self.__board[row][column] == player:
                        x = column
                        y = row
                        nr_of_pieces = 0

                        while 0 <= x < self.columns and 0 <= y < self.rows and self.__board[y][x] == player:
                            nr_of_pieces += 1
                            x += x_axis[i]
                            y += y_axis[i]

                        if nr_of_pieces >= 4:
                            return True

        return False

    def get_board_console(self):
        board = []
        i = -1
        for row in range(self.rows-1, -1, -1):
            board.append([])
            i += 1
            for column in range(self.columns-1, -1, -1):
                if self.__board[row][column] == 0:
                    board[i].append('O')
                else:
                    board[i].append(self.__board[row][column].color[0])

        return board

    def get_board(self):
        board = []
        i = -1
        for row in range(self.rows - 1, -1, -1):
            board.append([])
            i += 1
            for column in range(self.columns - 1, -1, -1):
                if self.__board[row][column] == 0:
                    board[i].append(Chip((0, 0, 0), 'None'))
                else:
                    board[i].append(self.__board[row][column])

        return board

    def get_different_column(self, new_mask):
        old_mask = self.mask
        for row in range(self.rows):
            for column in range(self.columns):
                if new_mask % 3 != old_mask % 3:
                    return column
                old_mask //= 3
                new_mask //= 3

    def clear(self):
        self.mask = 0
        self.__board = []
        self.mask_to_board()
