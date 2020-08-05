import os
WIDTH, HEIGHT = 7, 6


# BOARD AND RENDERING
def init_board(w=7, h=6):
    return [[None for i in range(0, w)] for j in range(0, h)]


def whatever(w=3, h=3):
    board = [[(i, j) for i in range(0, w)] for j in range(0, h)]
    return board


def index_board(w, h):
    b = init_board(w, h)
    count = 0
    for i in range(h):
        for j in range(w):
            b[i][j] = count
            count += 1
    return b


def render(board):
    print("  ", end="")
    for i in range(0, WIDTH):
        print(i, end="")
    print("\n  ", end="")
    for i in range(0, WIDTH):
        print("-", end="")
    print("")
    for i in range(0, HEIGHT):
        print(i, end="")
        print("|", end="")
        for j in range(0, WIDTH):
            if board[i][j] == "X":
                print("X", end="")
            elif board[i][j] == "O":
                print("O", end="")
            else:
                print(" ", end="")
        print("|")
    print("  ", end="")
    for i in range(0, WIDTH):
        print("-", end="")
    print("")


# MOVE
def get_y(board, move):
    y = len(board)-1
    for i in range(HEIGHT):
        if board[i][move] is not None:
            return i - 1
    return y


def get_move(board):
    move_x = int(input("Enter x coordinate: "))
    return [move_x, get_y(board, move_x)]


def is_valid_move(board, cord):
    if cord[0] >= WIDTH or cord[1] >= HEIGHT or cord[0] < 0 or cord[1] < 0 \
            or board[cord[1]][cord[0]] is not None:
        return False
    else:
        return True


def make_move(board, coordinates, player):
    if is_valid_move(board, coordinates):
        new_board = board
        new_board[coordinates[1]][coordinates[0]] = player
        return new_board
    else: raise Exception("Invalid move")


# CHECK BOARD
def is_same(arr):
    char, flag = arr[0], True
    for i in range(0, len(arr)):
        if arr[i] != char or arr[i] is None:
            flag = False
    if flag: return [flag, char]
    else: return [flag]


def get_vertical_families(board, f_size=4):
    columns = [[col[i] for col in board] for i in range(WIDTH)]
    return [[[columns[i][k] for k in range(j, j + f_size)] for j in range(HEIGHT - f_size + 1)] for i in range(WIDTH)]


def get_horizontal_families(board, f_size=4):
    return [[[board[i][k] for k in range(j, j + f_size)] for j in range(WIDTH - f_size + 1)] for i in range(HEIGHT)]


def get_diagonal_rl(board, f_size=4):
    return [[[board[i + m][k] for (k, m) in zip(range(j, -1, -1), range(f_size))] for j in range(WIDTH - f_size, WIDTH)]
            for i in range(HEIGHT - f_size + 1)]


def get_diagonal_lr(board, f_size=4):
    return [
        [[board[i + m][k] for (k, m) in zip(range(j, j + f_size), range(f_size))] for j in range(WIDTH - f_size + 1)]
        for i in range(HEIGHT - f_size + 1)]


def check_win(cols, vertical, dig_lr, dig_rl):
    win_flag, char = False, None
    for i in range(0, len(cols)):
        for j in range(len(cols[0])):
            if is_same(cols[i][j])[0]:
                win_flag, char = True, is_same(cols[i][j])[1]
    for i in range(0, len(vertical)):
        for j in range(len(vertical[0])):
            if is_same(vertical[i][j])[0]:
                win_flag, char = True, is_same(vertical[i][j])[1]
    for i in range(len(dig_lr)):
        for j in range(len(dig_lr[0])):
            if is_same(dig_lr[i][j])[0]:
                win_flag, char = True, is_same(dig_lr[i][j])[1]
    for i in range(len(dig_rl)):
        for j in range(len(dig_rl[0])):
            if is_same(dig_rl[i][j])[0]:
                win_flag, char = True, is_same(dig_rl[i][j])[1]
    if win_flag:
        return [win_flag, char]
    else:
        return [win_flag]


def check_full(board):
    full_flag = True
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] is None:
                full_flag = False
    return full_flag


def display_end(end_state, winner=None):
    if end_state == "Win": print("Congratulations! The winner is {}!".format(winner))
    elif end_state == "Draw": print("It is a draw! Want to play again? ")


def game(board, count=0):
    while True:
        os.system("cls")
        render(board)
        ver, hor, dig1, dig2 = get_vertical_families(board), get_horizontal_families(board), \
                               get_diagonal_lr(board), get_diagonal_rl(board)
        if check_win(ver, hor, dig1, dig2)[0]:
            display_end("Win", check_win(ver, hor, dig1, dig2)[1])
            break
        elif check_full(board):
            display_end("Draw")
            break
        else:
            move = get_move(board)
            if count % 2 == 0:
                board = make_move(board, move, "X")
            else:
                board = make_move(board, move, "O")
            count += 1


if __name__ == "__main__":
    game_board = init_board(WIDTH, HEIGHT)
    game(game_board)
    quit()
