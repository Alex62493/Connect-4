"""
I wrote something here, but my computer crashed and I dont want to write it again, so here is the gist of it
Chip used to play.
it has: Color - #Hex_Number - string
        Player - HumanPlayer1/HumanPlayer2/Computer - String

The user input has no interaction with this class so there is no need for validation
"""


class Chip:

    def __init__(self, color, player):
        self.__color = color
        self.__player = player

    @property
    def color(self):
        return self.__color

    @property
    def player(self):
        return self.__player
