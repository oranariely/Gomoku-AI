import numpy as np
from sequence_counter import SequenceCounter
import sys
SYM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E']
BLACK = 1
WHITE = 2


class GameBoard(object):
    """Game board."""

    ATTACK_WEIGHTS = 1.3
    DEFENCE_WEIGHTS = 1.3

    def __init__(self, board=None, indc_set=None, filled_cell_set=None, white_counter=None, black_counter=None,
                 last_action=None, move_counter=0):

        '''board'''
        # board is a 15*15 array: each posision is initially set to be 0
        if board is not None:
            self.board = np.array(board)
        else:
            self.board = np.zeros((15, 15), dtype=int)
        if indc_set:
            self.free_indexes = set(indc_set)
        else:
            self.free_indexes = set()
            self.free_indexes.add((7, 7))
        if filled_cell_set:
            self.filled = set(filled_cell_set)
        else:
            self.filled = set()

        # store positions of 5 stones in a line
        '''evaluator and black and white counters'''
        if not white_counter:
            self.white_counter = SequenceCounter(2)
        else:
            self.white_counter = white_counter.__copy__()
        if not black_counter:
            self.black_counter = SequenceCounter(1)
        else:
            self.black_counter = black_counter.__copy__()

        '''last action and move counter'''
        self.move_counter = move_counter
        if not last_action:
            self.last_action = (-1, -1)
        else:
            self.last_action = last_action

        self.game_over = False
        self.won = {}

    def generate_successor(self, turn, action):
        successor = GameBoard(board=self.board, indc_set=self.free_indexes, filled_cell_set=self.filled,
                              white_counter=self.white_counter, black_counter=self.black_counter, last_action=self.last_action)
        successor.apply_action(action, turn)
        return successor

    def apply_action(self, action, turn):
        '''changing coord in board'''
        self.board[action[0], action[1]] = turn
        self.last_action = action
        '''update free_indexes set and filled'''
        row = action[0]
        col = action[1]
        other = [(row + 1, col + 1), (row + 1, col), (row, col + 1), (row - 1, col - 1),
                 (row - 1, col), (row, col - 1), (row + 1, col - 1), (row - 1, col + 1)]
        for coord in other:
            if self.check_cell_indx(coord[0], coord[1]) == 0:
                self.free_indexes.add(coord)
        self.filled.add(action)
        self.free_indexes.remove(action)
        self.move_counter += 1
        if turn == BLACK:  # black
            self.black_counter.update_profit(self, action)
            self.white_counter.update_harm(self, action)
        elif turn == WHITE:  # white
            self.white_counter.update_profit(self, action)
            self.black_counter.update_harm(self, action)
        else:
            raise Exception("turn not 1 or 2")

    def get_actions_to_explore(self):
        return self.free_indexes

    def get_legal_actions(self):
        """Generate all legal moves for the current board"""
        return [tuple(m) for m in np.argwhere(self.board == 0)]

    def reset(self):
        """Clear the board (set all position to 0)."""
        self.board = np.zeros((15, 15))

    def get(self, row, col):
        """Get the value at a coord.
        if out of bounds - return 0 (empty coord)"""

        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return 0
        return self.board[row, col]

    def check_cell_indx(self, row, col):
        """Get the value at a coord.
        if out of bounds - return 0 (empty coord)"""

        if row < 0 or row >= 15 or col < 0 or col >= 15:
            return -1
        return self.board[row, col]

    def update_state(self, move, turn):
        """

        :param move: the move to update
        :param turn: 1 for black, 2 for white
        :return:
        """
        self.board[move[0], move[1]] = turn

    def check(self, row, col):
        """Check if there is a winner.

        assume (row,col) fill with 1 or 2 - check after assignment
        Returns:
            0-no winner, 1-black wins, 2-white wins
        """
        board = self.board

        # check in 4 directions
        # a coordinate stands for a specific direction, imagine the direction of a coordinate
        # relative to the origin on xy-axis

        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))

        # if no stone is on the position, don't need to consider this position

        # value-value at a coord, i-row, j-col
        value = board[row][col]
        # check if there exist 5 in a line
        for d in dirs:
            x, y = row, col
            count = 1
            for _ in range(1, 5):
                x += d[0]
                y += d[1]
                if self.get(x, y) != value:
                    break
                count += 1
            x, y = row, col
            for _ in range(1, 5):
                x -= d[0]
                y -= d[1]
                if self.get(x, y) != value:
                    break
                count += 1
            # if 5 in a line, store positions of all stones, return value
            if count >= 5:
                self.won = {}
                r, c = row, col
                for _ in range(5):
                    self.won[(r, c)] = 1
                    r += d[0]
                    c += d[1]
                return value
        return 0

    # def board(self):
    #     """Return the board array."""
    #     return self.board

    def show(self):
        """Output current board on terminal."""
        print('  0 1 2 3 4 5 6 7 8 9 A B C D E')
        for col in range(len(SYM)):
            sys.stdout.write(SYM[col] + " ")
            for row in range(15):
                ch = self.board[row][col]
                if ch == 0:
                    sys.stdout.write('.' + " ")
                elif ch == 1:
                    sys.stdout.write("X" + " ")
                elif ch == 2:
                    sys.stdout.write('O' + " ")

            print()

    def check_winner_by_values(self, turn):
        """Checks if someone won by black and white values
         @return np.inf and -np.inf if {turn} player won / lost accordingly """
        if turn == 1:
            if self.black_counter >= np.inf or self.white_counter <= -np.inf:
                return np.inf
            elif self.black_counter <= -np.inf or self.white_counter >= np.inf:
                return -np.inf
        elif turn == 2:
            if self.white_counter >= np.inf or self.black_counter <= -np.inf:
                return np.inf
            elif self.white_counter <= -np.inf or self.black_counter >= np.inf:
                return np.inf

        return None
