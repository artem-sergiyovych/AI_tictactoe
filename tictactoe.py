
import math

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
    count = sum(1 for row in board for cell in row if cell != EMPTY)
    return O if count % 2 == 1 else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")

    new_board = [row[:] for row in board]  # create a copy of the board
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(2, 0), (1, 1), (0, 2)]
    ]

    for combination in winning_combinations:
        values = [board[i][j] for i, j in combination]
        if values == [X, X, X]:
            return X
        if values == [O, O, O]:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)

    return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    value = -math.inf
    best_move = None

    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > value:
            value = min_val
            best_move = action

    return value, best_move


def min_value(board):
    if terminal(board):
        return utility(board), None

    value = math.inf
    best_move = None

    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < value:
            value = max_val
            best_move = action

    return value, best_move
