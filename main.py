from domain.chip import Chip
from board.board import Board
from service.connect4 import Connect4
from ui.gui.menu import GUI


def start():
    ui_mode()


def ui_mode():
    player1 = Chip((255, 0, 0), 'Player1')
    player2 = Chip((255, 255, 0), 'Player2')
    board = Board(player1, player2)
    service = Connect4(player1, player2, board)
    gui = GUI(service)


start()
