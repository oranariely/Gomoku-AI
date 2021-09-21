import numpy as np
import abc


PRINT_MOVES_VALUES = False


class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_board, turn):
        return

    def stop_running(self):
        pass


def return_max_dict(moves_dict):
    '''
    return the item of the maximal value in a dictionary
    if few moves has this value, return one of them randomly
    :return: the move that has the maximum move value
    '''
    max_moves = []
    max_value = -np.inf
    for move in moves_dict:
        if max_value < moves_dict[move]:
            max_moves = [move]
            max_value = moves_dict[move]
        elif max_value == moves_dict[move]:
            max_moves.append(move)
    return random.choice(max_moves)


def return_max(successors_values):
    '''
    :param successors_values: list of tuple: (successor, value)
    :return: tuple with maximal value
    '''
    if len(successors_values) == 0:
        return -np.inf
    return max(successors_values)


def return_min(successors_values):
    '''
    :param successors_values: list of tuple: (successor, value)
    :return: tuple with maximal value
    '''
    if len(successors_values) == 0:
        return -np.inf
    return min(successors_values)


def switch_turn(turn):
    if turn == 1:
        return 2
    return 1


from game_board import GameBoard
import random


def eval(game_board):
    turn = game_board.board[game_board.last_action]
    attack = 1.3
    if turn == 1:
        return game_board.ATTACK_WEIGHTS * game_board.black_counter.evaluate() - game_board.white_counter.evaluate()
    elif turn == 2:
        return game_board.ATTACK_WEIGHTS * game_board.white_counter.evaluate() - game_board.black_counter.evaluate()
    else:
        raise Exception("turn not 1 or 2")


def eval_tree(game_board):
    '''
    evaluation function for the order to of actions to explore in the tree
    '''

    turn = game_board.board[game_board.last_action]
    if turn == 1:
        return game_board.black_counter.evaluate() - game_board.DEFENCE_WEIGHTS * game_board.black_counter.evaluate(game_board.white_counter)
    elif turn == 2:
        return game_board.white_counter.evaluate() - game_board.DEFENCE_WEIGHTS * game_board.white_counter.evaluate(game_board.black_counter)
    else:
        raise Exception("turn not 1 or 2")


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    DEPTH = 1

    def __init__(self, depth=DEPTH):
        self.evaluation_function = eval
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_board, turn):
        return


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def rec_alpha_beta(self, turn, depth, game_board, alpha, beta):
        '''
        a recursive function to calculate alpha beta pruning
        :param depth: tracking our depth in the tree
        :param game_board: The state of the game
        :return: value of state according to alpha beta
        '''
        state_value = self.evaluation_function(game_board)
        if depth == 0:
            return state_value
        if state_value == np.inf:  # turn won
            return state_value
        # minimize
        if round(depth) != depth:  # depth = something.5
            opp = switch_turn(turn)
            min_value = np.inf
            moves_values = dict()  # for debug
            successors = [game_board.generate_successor(opp, action) for action in game_board.get_actions_to_explore()]
            sorted_successors = sorted(successors, key=eval_tree, reverse=True)
            for successor in sorted_successors:
                ''' return -value becuase it returns the value for the opponent which is (- our value) '''
                move_value = -self.rec_alpha_beta(opp, depth - 0.5, successor, alpha, beta)
                if move_value == -np.inf:
                    return -np.inf
                moves_values[successor.last_action] = move_value  # for debug
                min_value = min(min_value, move_value)
                if min_value <= alpha:
                    break  # not to continue iterating through child's (other moves)
                beta = min_value  # update beta: we found new minimal value in child's
            return min_value

        # maximize
        else:
            max_value = -np.inf
            moves_values = dict()  # for debug
            successors = [game_board.generate_successor(turn, action) for action in game_board.get_actions_to_explore()]
            sorted_successors = sorted(successors, key=eval_tree, reverse=True)
            for successor in sorted_successors:  # game_board.get_actions_to_explore():
                move_value = self.rec_alpha_beta(turn, depth - 0.5, successor, alpha, beta)
                moves_values[successor.last_action] = move_value  # for debug
                if move_value == np.inf:
                    return np.inf
                if move_value > max_value:
                    max_value = move_value
                if max_value >= beta:
                    break  # nor to continue iterating through child's (other moves)
                alpha = max_value  # update alpha: we found new maximum value in child's
            return max_value

    def get_action(self, game_board, turn):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        if no moves left - return None
        """
        moves = []
        moves_values = dict()  # for debug
        best_score = -np.inf
        successors = [game_board.generate_successor(turn, action) for action in game_board.get_actions_to_explore()]
        sorted_successors = sorted(successors, key=eval_tree, reverse=True)
        for successor in sorted_successors:
            move_value = self.rec_alpha_beta(turn, self.depth - 0.5, successor, alpha=(-np.inf), beta=(np.inf))
            moves_values[successor.last_action] = move_value  # for debug
            if move_value > best_score:
                moves = [successor.last_action]
                best_score = move_value
            elif move_value == best_score:
                moves.append(successor.last_action)
            elif move_value == np.inf:  # new
                return successor.last_action
            if PRINT_MOVES_VALUES:
                print("move: ", successor.last_action, " value: ", move_value)
        if not moves:  # didn't found a legal move
            return tuple((-1, -1))  # no more moves
        print("move counter", game_board.move_counter)
        return random.choice(moves)
