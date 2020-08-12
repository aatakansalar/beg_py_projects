import random as rand
from tic_tac_toe import *
from t_board import *


cache = {}


def has_win_move(arr, char, num=2):
    count = 0
    for i in range(0, len(arr)):
        if arr[i] == char:
            count += 1
    return [True, arr.index(None)] if count == num and None in arr else [False]


def get_winning_move(board, char):
    cols, digs = get_col_fam(board), get_dig_fam(board)
    for i in range(0, len(cols)):
        if has_win_move(cols[i], char, 2)[0]:
            return [True, [i, has_win_move(cols[i], char, 2)[1]]]
        if has_win_move(board[i], char, 2)[0]:
            return [True, [has_win_move(board[i], char, 2)[1], board.index(board[i])]]
    if has_win_move(digs[0], char, 2)[0]:
        return [True, [has_win_move(digs[0], char, 2)[1], has_win_move(digs[0], char, 2)[1]]]
    if has_win_move(digs[1], char, 2)[0]:
        return [True, [2 - has_win_move(digs[1], char, 2)[1], has_win_move(digs[1], char, 2)[1]]]
    return [False]


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


def random_ai(board, char_1, char_2):
    poss_moves = get_valid_moves(board)
    random = rand.randrange(len(poss_moves))
    return poss_moves[random]


def win_ai(board, char_1, char_2):
    if get_winning_move(board, char_1)[0]:
        return get_winning_move(board, char_1)[1]
    else:
        return random_ai(board, char_1, char_2)


def win_lose_ai(board, char_1, char_2):
    if get_winning_move(board, char_1)[0]:
        return get_winning_move(board, char_1)[1]
    elif get_winning_move(board, char_2)[0]:
        return get_winning_move(board, char_2)[1]
    else:
        return random_ai(board, char_1, char_2)


# MINIMAX
def minimax_score(board, current_player, player):
    if check_win(board)[0] and check_win(board)[1] == player:
        return 10
    elif check_win(board)[0] and check_win(board)[1] == get_opponent(player):
        return -10
    elif check_full(board):
        return 0

    legal_moves = get_valid_moves(board)
    scores = []

    for move in legal_moves:
        new_board = make_move(board, move, current_player)
        opponent = get_opponent(current_player)
        score = minimax_score(new_board, opponent, player)
        scores.append(score)

    if current_player == player:
        return max(scores)
    else:
        return min(scores)


def minimax_ai(board, char1, char2):
    high_score = None
    best_move = None
    legal_moves = get_valid_moves(board)
    player = char1
    for move in legal_moves:
        new_board = make_move(board, move, player)
        opponent = get_opponent(player)
        score = cached_minimax_score(new_board, opponent, player)
        if high_score is None or score > high_score:
            best_move = move
            high_score = score
    return best_move


def cached_minimax_score(board, current_player, player):
    board_cache_keyword = str(board)
    if board_cache_keyword not in cache:
        score = minimax_score(board, current_player, player)
        cache[board_cache_keyword] = score
    return cache[board_cache_keyword]