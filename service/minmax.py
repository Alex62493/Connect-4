"""
This file will have a class which will create a dictionary of moves
d['current_mask'] = best_possible_mask

This dict will be created trough the min-max algorithm
If it will occupy too much space, then i will use alpha-beta pruning, which will cost time, but not use as much space

Upon further research I found out that I'm an idiot
It take to much time to search trough every move from any point, so I will use a depth system
"""
from board.board import Mask


class MinMax:

    def __init__(self):
        self.__current_move = 1
        self.__next_move = 0

    @property
    def next_move(self):
        return self.__next_move

    @property
    def inf(self):
        return 100

    @property
    def depth(self):
        return 5

    def min_max(self, nr, alpha, beta, depth):
        mask = Mask(nr)
        move = self.__current_move % 2

        if move == 0:
            maximum = -self.inf
            max_move = 0

            won = mask.check_mask_for_win(1)

            if won:
                return -(22 - self.__current_move//2), nr

            if depth == 0:
                return 22 - self.__current_move // 2 - mask.approximate_points(2), nr

            for column in mask.get_random_colon_list():
                for row in range(mask.rows):
                    if mask.check_if_move_possible(row, column):
                        next_move = mask.simulate_chip_drop(row, column, 2)
                        self.__current_move += 1
                        current_score = self.min_max(next_move, alpha, beta, depth-1)[0]
                        self.__current_move -= 1
                        if current_score > maximum:
                            maximum = current_score
                            max_move = next_move
                            alpha = max(alpha, maximum)
                        break
                if beta <= maximum:
                    break

            return maximum, max_move

        if move == 1:
            minimum = self.inf
            min_move = 0

            won = mask.check_mask_for_win(2)

            if won:
                return 22 - self.__current_move//2, nr

            if self.__current_move == 43:
                return 0, nr

            if depth == 0:
                return -(22 - self.__current_move // 2 - mask.approximate_points(2)), nr

            for column in mask.get_random_colon_list():
                for row in range(mask.rows):
                    if mask.check_if_move_possible(row, column):
                        next_move = mask.simulate_chip_drop(row, column, 1)
                        self.__current_move += 1
                        current_score = self.min_max(next_move, alpha, beta, depth-1)[0]
                        self.__current_move -= 1
                        if current_score < minimum:
                            minimum = current_score
                            min_move = next_move
                            beta = min(beta, minimum)
                        break
                if alpha >= minimum:
                    break

            return minimum, min_move

    def start_min_max_from(self, nr, current_move):
        self.__current_move = current_move
        self.__next_move = self.min_max(nr, -self.inf, self.inf, self.depth)[1]
