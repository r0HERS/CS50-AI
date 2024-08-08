"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    X_count = 0
    O_count = 0
    
    for row in range(len(board)):
        for  cell in range(len(board[row])):
            if board[row][cell] == X:
                X_count += 1
            elif board[row][cell] == O:
                O_count += 1

    if X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for row in range(len(board)):
        for  cell in range(len(board[row])):
            if board[row][cell] == EMPTY:
                actions.add((row,cell))


    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    board_copy = copy.deepcopy(board)

    i,j = action

    if action in actions(board):
        board_copy[i][j] = player(board)
        return board_copy
    else:
        raise NameError('Not valid action')



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
        
        
    for collum in range(len(board)):
        if board[0][collum] == board[1][collum] == board[2][collum] and board[0][collum] is not None:
            return board[0][collum]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]          


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    if len(actions(board)) == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    final_state = winner(board)

    if final_state == X:
        return 1
    elif final_state == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    current_player = player(board)

    if current_player == X:
        best_value = -math.inf
        best_move = None
        for action in actions(board):
            move_value = min_value(result(board, action))
            if move_value > best_value:
                best_value = move_value
                best_move = action
        return best_move
    else:
        best_value = math.inf
        best_move = None
        for action in actions(board):
            move_value = max_value(result(board, action))
            if move_value < best_value:
                best_value = move_value
                best_move = action
        return best_move

def max_value(board):
    v = -math.inf

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

