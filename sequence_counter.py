import numpy as np

DIRS = ((1, -1), (1, 0), (1, 1), (0, 1))
DIRS_8 = [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, -1), (0, -1), (-1, 0)]

HALF = 0
LIVE = 1

"""

    this class is built similar too the previous evaluate class (I actually copied the functions and changed little things there), 
    Except that it doesn't update the the values, it update the condition of a turn (1 or 2, black or white)
    
    self.counter is a 2 by 5 matrix where: 
        the i columns (0 to 4) indicate the sequnce length, 
        the first row is counter of one side (half) bounded sequence
        the second row is counter of two sided free sequence
    for example:
        self.counter[0, 4] = 2 , means that {turn} has 2 sequences of length 4 that is one side bounded
        self.counter[1, 2] = 3 , means that {turn} has 3 sequences of length 2 that are free from both sides
        
"""


class SequenceCounter:
    """
    class for counting the sequences for a specific agent
    """

    ''' a matrix that we want to multiply element-wise with self.counter and then sum it to evaluate the board
        WEIGHTS[0, j] = the value of a half bounded (one side) sequence of length j to the player board value
        WEIGHTS[1, j] = the value of a live (two side free) sequence of length j to the player board value'''
    WEIGHTS = np.array([[0, 0, 500, 25000, 100000], [0, 0, 1000, 100000, 2000000]])  # Half , Live

    def __init__(self, turn, weights=WEIGHTS):
        self.counter = np.zeros((2, 5))
        self.turn = turn
        self.won = False
        self.weights = weights

    def __copy__(self):
        new = SequenceCounter(self.turn)
        new.counter = self.counter.__copy__()
        new.won = self.won
        return new

    def update_counter(self, type, seq, val):
        """
        Update the counter
        Do not count sequences of length 0 or 1
        :param type: HALF or LIVE
        :param seq: The sequence length
        :param val: +1 or -1 , for add or remove a sequence accordingly
        """
        if seq <= 1:
            return
        self.counter[type, seq] += val

    def evaluate(self, other_counter=None):
        """multiply the sequences array with the weights array and sum the values.
        This is the value of the board"""
        if not other_counter:
            if self.won:
                return np.inf
            return np.sum(np.multiply(self.counter, self.weights))
        else:  # other counter
            if other_counter.won:
                return np.inf
            return np.sum(np.multiply(other_counter.counter, self.weights))

    def update_harm(self, game_board, action):
        """
        Evaluate the harm the other player caused to self
        :param action: the last move of the opponent
        """
        turn = self.turn
        for d1, d2 in DIRS_8:
            x = action[0] + d1
            y = action[1] + d2
            other_val = game_board.check_cell_indx(x, y)
            if other_val != turn:  # he didn't cause harm in this direction, didn't block me here
                continue
            seq_length, bounded = self.find_seq_and_bounded(game_board, action, other_val, d1, d2)
            if bounded:  # killed a half live one
                self.update_counter(HALF, seq_length, -1)
            else:  # still alive # one side
                self.update_counter(LIVE, seq_length, -1)
                self.update_counter(HALF, seq_length, 1)

    def update_profit(self, game_board, action):
        """
        Update values for turn = self.turn -> for profits for player who played
        """
        row, col = action
        for d1, d2 in DIRS:
            left, l_dead = self.find_seq_and_bounded(game_board, action, self.turn, d1, d2)
            right, r_dead = self.find_seq_and_bounded(game_board, action, self.turn, -d1, -d2)
            seq_length = left + right + 1
            '''chack if won - a sequence length 5 or more'''
            if seq_length >= 5:
                self.won = True
                # Do not update counter because it is useless
                return
            '''update counter according to board situation for the direction'''
            if not (l_dead and r_dead):  # at least one side is not dead
                if not l_dead and not r_dead:  # both sides are open, LIVE
                    self.update_counter(LIVE, seq_length, 1)
                    self.update_counter(LIVE, right, -1)
                    self.update_counter(LIVE, left, -1)
                else:  # One side is dead, DEAD
                    self.update_counter(HALF, seq_length, 1)
                    # now: check if was half bounded before :( 0 1 1 _ 2, put 1 in _)
                    if game_board.check_cell_indx(row + d1, col + d2) not in [self.turn, 0] and \
                            game_board.check_cell_indx(row - d1, col - d2) not in [self.turn, 0]:
                        # wasn't half bounded before( = other turn or -1)
                        self.update_counter(LIVE, left, -1)
                        self.update_counter(LIVE, right, -1)
                    else:  # was half bounded before
                        '''check both side if were bounded ( one true and one false) and update accordingly'''
                        if l_dead:  # left
                            self.update_counter(HALF, left, -1)
                        else:
                            self.update_counter(LIVE, left, -1)
                        if r_dead:  # right
                            self.update_counter(HALF, right, -1)
                        else:
                            self.update_counter(LIVE, right, -1)
            else:  # both sides are dead
                self.update_counter(HALF, left, -1)
                self.update_counter(HALF, right, -1)

    def find_seq_and_bounded(self, game_board, action, turn, d1, d2):
        """
        find length of sequence .exclude the current action position
        :return: size of sequence, if its bounded
        """
        is_dead = True
        x = action[0] + d1
        y = action[1] + d2
        size_cons = 0
        # while the stone in the same color
        while game_board.check_cell_indx(x, y) == turn:
            size_cons += 1
            x += d1
            y += d2

        if game_board.check_cell_indx(x, y) == 0:
            is_dead = False

        return size_cons, is_dead


def evaluate(counter_1, counter_2):
    return counter_1.evaluate() - counter_2.evaluate()
