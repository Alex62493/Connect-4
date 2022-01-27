from ui.console import Console
from domain.chip import Chip
from board.board import Board
from service.connect4 import Connect4
from ui.gui.menu import GUI


def start():
    correct = False

    while not correct:
        mode = input('GUI or console\n')

        if mode == 'GUI':
            ui_mode()
            correct = True
        elif mode == 'console':
            console_mode()
            correct = True


def ui_mode():
    player1 = Chip((255, 0, 0), 'Player1')
    player2 = Chip((255, 255, 0), 'Player2')
    board = Board(player1, player2)
    service = Connect4(player1, player2, board)
    gui = GUI(service)


def console_mode():
    player1 = Chip('Red', 'Player1')
    player2 = Chip('Yellow', 'Player2')
    board = Board(player1, player2)
    service = Connect4(player1, player2, board)
    console = Console(service)


start()
