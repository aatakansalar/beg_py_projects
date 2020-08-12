import os, sys
from t_board import *
from ai import *

WIDTH, HEIGHT = 3, 3

"""
Example Uses: 

python tic_tac_toe.py minimax_ai minimax_ai stats 1
python tic_tac_toe.py minimax_ai minimax_ai game
python tic_tac_toe.py random_ai minimax_ai game
python tic_tac_toe.py win_ai win_lose_ai stats 100
"""
# TODO Alpha-beta pruning
# TODO  Create a function to get pre-calculated JSON list file of best moves to solve the time problem


def render(board):
    print("  ", end="")
    for i in range(0, WIDTH):
        print(i, end="")
    print("")
    print("  ---")
    for i in range(0, WIDTH):
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
    print("  ---")


def get_opponent(player):
    return 'O' if player == 'X' else 'X'


def display(end_state, winner=None):
    if end_state == "Win":
        print("Congratulations! The winner is {}!".format(winner))
    elif end_state == "Draw":
        print("It is a draw! Want to play again? ")


# GAME LOOP
def game(board, count=0):
    while True:
        os.system("cls")
        render(board)
        if check_win(board)[0]:
            display("Win", check_win(board)[1])
            break
        elif check_full(board):
            display("Draw")
            break
        else:
            if count % 2 == 0:
                move = move_wrapper(board, "X", "O", globals()[sys.argv[1]])
                board = make_move(board, move, "X")
                t.sleep(0.2)
            else:
                move = move_wrapper(board, "O", "X", globals()[sys.argv[2]])
                board = make_move(board, move, "O")
                t.sleep(0.2)
            count += 1


def game_for_stats(board, count=0):
    while True:
        if check_win(board)[0]:
            if check_win(board)[1] == "X":
                return 1
            elif check_win(board)[1] == "O":
                return 2
        elif check_full(board):
            return 0
        else:
            if count % 2 == 0:
                move = move_wrapper(board, "X", "O", globals()[sys.argv[1]])
                board = make_move(board, move, "X")
            else:
                move = move_wrapper(board, "O", "X", globals()[sys.argv[2]])
                board = make_move(board, move, "O")
            count += 1


def play_stats(times):
    x, y, d, count = 0, 0, 0, 0
    while count < times:
        board = init_board(WIDTH, HEIGHT)
        ret = game_for_stats(board)
        if ret == 2:
            y += 1
        elif ret == 1:
            x += 1
        else:
            d += 1
        count += 1
    print("X win count: ", x, "\nO win count: ", y, "\nDraw count: ", d)


if __name__ == "__main__":
    if sys.argv[3] == "stats":
        play_stats(int(sys.argv[4]))
        quit()
    elif sys.argv[3] == "game":
        game_board = init_board(WIDTH, HEIGHT)
        game(game_board)
        quit()
