"""
Tic Tac Toe Player
"""
from collections import Counter

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
    nump = Counter([p for row in board for p in row ]) 
    #Counter objects have a dictionary interface except that they return a zero count for missing items instead of raising a KeyError:
    '''
    if O in nump and nump[O]<nump[X]:
        return O
    if O not in nump and X in nump:
        return O
    else:
        return X
    '''
    if nump[O]<nump[X]:
        return O
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionset = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                actionset.add((row,col))

    return (actionset)
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0]>2:
        raise IndexError
    if action[1]>2:
        raise IndexError
    if board[action[0]][action[1]] is not None:
        raise ValueError
    boardcopy = copy.deepcopy(board)

    turn = player(board)
    boardcopy[action[0]][action[1]] = turn
    return boardcopy

    

    raise NotImplementedError

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #row winner

    nump = [Counter(row) for row in board]
    for i in range(3):
        if nump[i][X]>2:
            return X
        if nump[i][O]>2:
            return O    
            
    #col winner
    for col in range(3):
        if board[0][col] is not None:
            if board[0][col]==board[1][col] and board[1][col] == board[2][col]:
                return board[0][col]
                

    #diag winner
    if board[1][1] is not None:
        if board[0][0]==board[1][1] and board[1][1] == board[2][2]:
            return board[1][1]
   
        if board[0][2]==board[1][1] and board[1][1] == board[2][0]:
            return board[1][1]
 
    #no winner
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # wonnereds!
    if winner(board) is not None:
        return True

    # empty space left
    if any(None in row for row in board):
        return False
    
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #terminal returns true
    won = winner(board)
    if won is None:
        return 0
    if won == X:
        return 1
    
    return -1
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v = -999999
        maxval = maxv(board)
        for action in actions(board):
            v = max(v,minv(result(board, action)))
            if v == maxval:
                #print(action, v)
                return action


    else:
        v = 999999
        minval = minv(board)
        for action in actions(board):
            v = min(v,maxv(result(board, action)))
            if v == minval:
                #print(action, v)
                return action
    raise NotImplementedError


def maxv(board):
    v=-999999
    if terminal(board):
        return utility(board)

    for action in actions(board):

        v = max(v,minv(result(board, action)))
        #print(action, v, " max")
    return v

def minv(board):
    v=999999
    if terminal(board):
        return utility(board)

    for action in actions(board):

        v = min(v,maxv(result(board, action)))
        #print(action, v, " min")
    return v



