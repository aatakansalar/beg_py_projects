import os
import random
import sys
import time

import numpy as np

"""
Use: 
>> python life.py "rand" 100 100
options: rand(regular), vnn, reprod(reproduction), immortal, load
>> python life.py "vnn" 100 100
>> python life.py "reprod" 100 100
>> python life.py "immortal" 100 100
>> python life.py "load" "gosper_glider_gun.txt"

Tutorial-Link:https://robertheaton.com/2018/07/20/project-2-game-of-life/
"""


# NEW BOARD
def rand():
    r = random.random()
    if r >= 0.5:
        return 1
    else:
        return 0


# Creates an empty board
def dead_state(a: int, b: int):
    arr = np.arange(a*b).reshape(a, b)
    for x in range(0, a):
        for y in range(0, b):
            arr[x][y] = 0
    return arr


# Randomizes the board with rand()
def random_state(a: int, b: int):
    rand_state = dead_state(a,b)
    for x in range(0, a):
        for y in range(0, b):
            rand_state[x][y] = rand()
    return rand_state


# PRINTING THE BOARD

# Renders to terminal
def render(state):
    y = len(state)
    x = len(state[1])
    for a in range(0, x + 2) :
        if a != x+1:
            print("-", end="")
        else:
            print("-")
    for i in range(0, y):
        print("|", end="")
        for j in range(0, x):
            if state[i][j] == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print("|")
    for a in range(0, x + 2) :
        if a != x+1:
            print("-", end="")
        else:
            print("-")


# NEXT BOARD STATE FUNCTIONS

# Uses moore neighborhood
def neighbor_count(state, coordinates):
    x, y, count = coordinates[0], coordinates[1], 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not y+i < 0 and not y+i >= len(state) and not x + j < 0 and not x + j >= len(state[1]):
                if state[y + i][x + j] == 1:
                    count += 1
    if state[y][x] == 1:
        return count - 1
    else:
        return count


# Uses VNN Neighborhood
def neighbor_count_vnn(state, coordinates):
    x, y, count = coordinates[0], coordinates[1], 0
    for i in range(-2, 3):
        if not y + i < 0 and not y + i >= len(state):
            if state[y + i][x] == 1:
                count += 1
    for i in range(-2, 3):
        if not x + i < 0 and not x + i >= len(state[1]):
            if state[y][x + i] == 1:
                count += 1
    if state[y][x] == 1:
        return count - 2
    else:
        return count


def next_cell_state(state, coordinates, neighbor_func):
    if state[coordinates[1]][coordinates[0]] == 1:
        if neighbor_func(state, coordinates) == 0 or neighbor_func(state, coordinates) == 1:
            # dies on underpopulation
            return 0
        elif neighbor_func(state, coordinates) == 2 or neighbor_func(state, coordinates) == 3:
            # stays alive in the right population amount
            return 1
        elif neighbor_func(state, coordinates) > 3:
            # dies 'cause of overpopulation
            return 0
        else:
            # cell state unchanged
            return 1
    else:
        if neighbor_func(state, coordinates) == 3:
            # reproduction
            return 1
        else:
            # cell state unchanged
            return 0


def next_state_function(state):
    y, x = len(state), len(state[1])
    new_state = dead_state(y, x)
    for i in range(0, y):
        for j in range(0, x):
            new_state[i][j] = next_cell_state(state, (j, i), neighbor_count)
    return new_state


def next_state_vnn(state):
    y, x = len(state), len(state[1])
    new_state = dead_state(y, x)
    for i in range(0, y):
        for j in range(0, x):
            new_state[i][j] = next_cell_state(state, (j, i),neighbor_count_vnn)
    return new_state


def next_state_rand_reprod(state):
    y, x = len(state), len(state[1])
    new_state = dead_state(y, x)
    for i in range(0, y):
        for j in range(0, x):
            rand = random.random()
            if state[i][j] == 0 and rand > 0.7:
                new_state[i][j] = 1
            else:
                new_state[i][j] = next_cell_state(state, (j, i),neighbor_count)
    return new_state


def next_state_immortal(state):
    y, x = len(state), len(state[1])
    new_state = dead_state(y, x)
    for i in range(0, y):
        for j in range(0, x):
            if state[i][j] == 1:
                new_state[i][j] = 1
            else:
                new_state[i][j] = next_cell_state(state, (j, i),neighbor_count)
    return new_state


# LOAD FUNCTION
def to_initial_state(file: str):
    f = open(file, "r")
    Lines = f.readlines(),
    x, y = len(Lines[0][0]) - 1, len(Lines[0])
    i_state = dead_state(y, x)
    for i in range(0, y):
        for j in range(0, x):
            i_state[i][j] = Lines[0][i][j]
    return i_state


# INFINITE LOOP
def life(initial_state, next_func):
    next_state = initial_state
    while True:
        os.system("cls")
        render(next_state)
        next_state = next_func(next_state)
        time.sleep(0.02)


if __name__ == "__main__":
    # TODO - rid
    if sys.argv[1] == "rand":
        state = random_state(int(sys.argv[2]), int(sys.argv[3]))
        life(state, next_state_function)
    elif sys.argv[1] == "reprod":
        state = random_state(int(sys.argv[2]), int(sys.argv[3]))
        life(state, next_state_rand_reprod)
    elif sys.argv[1] == "immortal":
        state = random_state(int(sys.argv[2]), int(sys.argv[3]))
        life(state, next_state_immortal)
    elif sys.argv[1] == "vnn":
        state = random_state(int(sys.argv[2]), int(sys.argv[3]))
        life(state, next_state_vnn)
    elif sys.argv[1] == "load":
        if sys.argv[3] == "reg":
            life(to_initial_state(sys.argv[2]), next_state_function)
        elif sys.argv[3] == "reprod":
            life(to_initial_state(sys.argv[2]), next_state_rand_reprod)
        elif sys.argv[3] == "immortal":
            life(to_initial_state(sys.argv[2]), next_state_immortal)
        elif sys.argv[3] == "vnn":
            life(to_initial_state(sys.argv[2]), next_state_vnn)

