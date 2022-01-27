"""
The position class will have 2 entities: row and collum
I will also validate the values inside teh class, since it shouldn't be a problem in regards to the SRP

This exists for the sole reason that i might want to use chip.row and chip.column (int), but also chip.position
"""


class Position:

    def __init__(self, row, column):
        if not (0 <= row <= 5 and 0 <= column <= 6):
            raise ValueError('Row or column value are wrong/impossible')

        self.__row = row
        self.__column = column

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column
