import copy

WIDTH, HEIGHT = 3, 3


def init_board(w=3, h=3):
    board = [[None for i in range(0, w)] for j in range(0, h)]
    return board


def is_valid_move(board, coordinates):
    if coordinates[0] >= WIDTH or coordinates[1] >= HEIGHT or coordinates[0] < 0 or coordinates[1] < 0 \
            or board[coordinates[1]][coordinates[0]] is not None:
        return False
    else:
        return True


def get_valid_moves(board):
    legal_moves = list()
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if is_valid_move(board, [j, i]):
                legal_moves.append([j, i])
    return legal_moves


def get_move(board, char_1, char_2):
    move_x, move_y = int(input("Enter x coordinate: ")), int(input("Enter y coordinate: "))
    return [move_x, move_y]


def make_move(board, coordinates, player):
    new_board = copy.deepcopy(board)
    if is_valid_move(new_board, coordinates):
        new_board[coordinates[1]][coordinates[0]] = player
        return new_board
    else:
        raise Exception("Invalid move", coordinates, player)


def move_wrapper(board, char_1, char_2, function):
    return function(board, char_1, char_2)


# CHECK BOARD
def is_same(arr):
    char, flag = arr[0], True
    for i in range(0, len(arr)):
        if arr[i] != char or arr[i] is None:
            flag = False
    return [flag, char] if flag else [flag]


def get_col_fam(board):
    return [[col[i] for col in board] for i in range(len(board[0]))]


def get_dig_fam(board):
    return [[board[i][i] for i in range(len(board[0]))],
            [board[i][len(board[0]) - i - 1] for i in range(len(board[0]))]]


def check_win(board):
    cols, digs, win_flag, char = get_col_fam(board), get_dig_fam(board), False, None
    for i in range(0, len(cols)):
        if is_same(cols[i])[0]:
            win_flag, char = True, is_same(cols[i])[1]
        if is_same(board[i])[0]:
            win_flag, char = True, is_same(board[i])[1]
    for i in range(0, len(digs)):
        if is_same(digs[i])[0]:
            win_flag, char = True, is_same(digs[i])[1]
    return [win_flag, char] if win_flag else [win_flag]


def check_full(board):
    full_flag = True
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] is None:
                full_flag = False
    return full_flag
