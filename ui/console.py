"""
The console module
The main module will call either this module or the ui(tbd)

The player vs ai isn't functional yet
"""


class Console:

    def __init__(self, connect4):
        self.__serv = connect4
        self.start()

    def start(self):
        stop = False

        while not stop:
            self.__serv.clear()
            correct_input = False

            while not correct_input:
                try:
                    mode = int(input('Press 1 for Human vs Human and 2 for Human vs AI\n'))
                    if not 1 <= mode <= 2:
                        raise ValueError
                    correct_input = True
                except ValueError:
                    print('Incorrect input!')

            if mode == 1:
                self.player_vs_player()
            else:
                self.player_vs_ai()

            correct = False

            while not correct:
                mode = input('Play again? Y/N\n')

                if mode == 'Y':
                    correct = True
                elif mode == 'N':
                    stop = True
                    correct = True

    def player_vs_player(self):
        won = 0

        while won == 0 and self.__serv.played_chips < 42:
            correct_input = False

            while not correct_input:
                try:
                    column = int(input('Player 1:\n'))
                    self.__serv.play_player1(column)
                    correct_input = True
                except ValueError as msg:
                    print(msg)

            self.print_board()

            if self.__serv.check_win_player1():
                won = 1
                break

            correct_input = False

            while not correct_input:
                try:
                    column = int(input('Player 2:\n'))
                    self.__serv.play_player2(column)
                    correct_input = True
                except ValueError as msg:
                    print(msg)

            self.print_board()

            if self.__serv.check_win_player2():
                won = 2

        if won == 0:
            print('Draw')
        elif won == 1:
            print('Player 1 wins!')
        elif won == 2:
            print('Player 2 wins!')

    def player_vs_ai(self):
        won = 0

        while won == 0 and self.__serv.played_chips < 42:
            correct_input = False

            while not correct_input:
                try:
                    column = int(input('Player 1:\n'))
                    self.__serv.play_player1(column)
                    correct_input = True
                except ValueError as msg:
                    print(msg)

            self.print_board()

            if self.__serv.check_win_player1():
                won = 1
                break

            self.__serv.play_ai()

            print('\n')
            self.print_board()

            if self.__serv.check_win_player2():
                won = 2

        if won == 0:
            print('Draw')
        elif won == 1:
            print('Player 1 wins!')
        elif won == 2:
            print('Computer wins!')

    def print_board(self):
        board = self.__serv.get_board_console()
        for i in board:
            for j in i:
                print(j, end=' ')
            print('\n', end='')
