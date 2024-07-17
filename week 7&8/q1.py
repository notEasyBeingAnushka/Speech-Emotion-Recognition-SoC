import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging
import pygame

pygame.init()



logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):
        # check if the board position is a win for either players
        # Feel free to implement this in anyway if needed
        combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for comb in combinations:
            if self.board[comb[0]] == self.board[comb[1]] == self.board[comb[2]] != '0':
                return True
        return False
        # pass
        

    def is_draw(self):
        # check if the board position is a draw
        # Feel free to implement this in anyway if needed
        if '0' not in self.board:
            if not self.is_win():
                return True
        return False
        # pass


    def get_valid_actions(self):
        # get the empty squares from the board
        # Feel free to implement this in anyway if needed
        valid_actions = []
        for i in range(9):
            if self.board[i] == '0':
                valid_actions.append(i)
        return valid_actions
        # pass

    def is_terminal_history(self):
        # check if the history is a terminal history
        # Feel free to implement this in anyway if needed
        if self.is_win() or self.is_draw():
            return True
        return False
        # pass

    def get_utility_given_terminal_history(self):
        # Feel free to implement this in anyway if needed
        if self.is_win():
            if self.player == 'x':
                return 1
            else:
                return -1
        else:
            return 0
        # pass
        

    def update_history(self, action):
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        # Feel free to implement this in anyway if needed
        new_History = copy.deepcopy(self)
        new_History.history.append(action)
        new_History.board = new_History.get_board()
        new_History.player = new_History.current_player()
        return new_History
        # pass

strategy_dict_x = {}
strategy_dict_o = {}

def backward_induction(history_obj):
    """
    :param history_obj: Histroy class object
    :return: best achievable utility (float) for th current history_obj
    """
    # global strategy_dict_x, strategy_dict_o
    # TODO implement
    # (1) Implement backward induction for tictactoe
    # (2) Update the global variables strategy_dict_x or strategy_dict_o which are a mapping from histories to
    # probability distribution over actions.
    # (2a)These are dictionary with keys as string representation of the history list e.g. if the history list of the
    # history_obj is [0, 4, 2, 5], then the key is "0425". Each value is in turn a dictionary with keys as actions 0-8
    # (str "0", "1", ..., "8") and each value of this dictionary is a float (representing the probability of
    # choosing that action). Example: {”0452”: {”0”: 0, ”1”: 0, ”2”: 0, ”3”: 0, ”4”: 0, ”5”: 0, ”6”: 1, ”7”: 0, ”8”:
    # 0}}
    # (2b) Note, the strategy for each history in strategy_dict_x and strategy_dict_o is probability distribution over
    # actions. But since tictactoe is a PIEFG, there always exists an optimal deterministic strategy (SPNE). So your
    # policy will be something like this {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0} where
    # "0" was the one of the best actions for the current player/history.
    board_str = ''.join([str(history_obj.history[i]) for i in range(len(history_obj.history))])
    action_dict = {"0":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
    
    if history_obj.is_terminal_history():
        return history_obj.get_utility_given_terminal_history()
    
    if history_obj.player == 'x' and board_str in strategy_dict_x:
        return strategy_dict_x[board_str]
    
    if history_obj.player == 'o' and board_str in strategy_dict_o:
        return strategy_dict_o[board_str]
    
    if history_obj.player == 'x':
        v = -math.inf
        best_action = None
        for action in history_obj.get_valid_actions():
            new_history = history_obj.update_history(action)
            new_v = backward_induction(new_history)
            if new_v > v:
                v = new_v
                best_action = str(action)
                action_dict[best_action] = 1
        strategy_dict_x[board_str] = action_dict
        return v
    
    if history_obj.player == 'o':
        v = math.inf
        best_action = None
        for action in history_obj.get_valid_actions():
            new_history = history_obj.update_history(action)
            new_v = backward_induction(new_history)
            if new_v < v:
                v = new_v
                best_action = str(action)
                action_dict[best_action] = 1
        strategy_dict_o[board_str] = action_dict
        return v
    
    
    # TODO implement


def solve_tictactoe():
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    return strategy_dict_x, strategy_dict_o


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")
