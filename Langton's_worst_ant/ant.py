import os
import time
import sys

import numpy as np
import random as rand

"""
Use:
python ant.py 100 50 0
=> First two arguments modifies the board size, last argument changes the time the loop waits before refreshing

# TODO:
GUI, out of bounds stuff
"""


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ant:
    def __init__(self, coordinates, forward):
        self.coordinates = coordinates
        self.forward = forward

    def detect_direction(self, ):
        x, y = self.forward.x - self.coordinates.x, self.forward.y - self.coordinates.y
        return [x, y]

    def move_forward(self):
        direction = self.detect_direction()
        self.coordinates = self.forward
        self.forward = Coordinates(self.coordinates.x + direction[0], self.coordinates.y + direction[1])

    def turn_right(self, ):
        direction = self.detect_direction()
        if direction[0] == 0 and direction[1] == 1:
            self.forward.x, self.forward.y = self.coordinates.x - 1, self.coordinates.y
        elif direction[0] == 0 and direction[1] == -1:
            self.forward.x, self.forward.y = self.coordinates.x + 1, self.coordinates.y
        elif direction[0] == 1 and direction[1] == 0:
            self.forward.y, self.forward.x = self.coordinates.y + 1, self.coordinates.x
        elif direction[0] == -1 and direction[1] == 0:
            self.forward.y, self.forward.x = self.coordinates.y - 1, self.coordinates.x

    def turn_left(self):
        direction = self.detect_direction()
        if direction[0] == 0 and direction[1] == 1:
            self.forward.x, self.forward.y = self.coordinates.x + 1, self.coordinates.y
        elif direction[0] == 0 and direction[1] == -1:
            self.forward.x, self.forward.y = self.coordinates.x - 1, self.coordinates.y
        elif direction[0] == 1 and direction[1] == 0:
            self.forward.y, self.forward.x = self.coordinates.y - 1, self.coordinates.x
        elif direction[0] == -1 and direction[1] == 0:
            self.forward.y, self.forward.x = self.coordinates.y + 1, self.coordinates.x


# Creating the board
def init_board(a: int, b: int):
    arr = np.arange(a * b).reshape(a, b)
    for x in range(0, a):
        for y in range(0, b):
            arr[x][y] = 0
    return arr


def is_on_board(board, coordinates):
    x_board = len(board[1])
    y_board = len(board)
    if coordinates.x > x_board or coordinates.y > y_board or coordinates.x < 0 or coordinates.y < 0:
        return False
    else:
        return True


# Ant
def get_random_point(board):
    x_rand, y_rand = rand.randrange(len(board[0])), rand.randrange(len(board))
    coordinate = Coordinates(x_rand, y_rand)
    forward = Coordinates(x_rand, y_rand + 1)
    return [coordinate, forward]


def ant_move(board, ant):
        cell = board[ant.coordinates.y][ant.coordinates.x]
        if cell == 0:
            # White
            ant.turn_right()
            board[ant.coordinates.y][ant.coordinates.x] = 1
            ant.move_forward()
        elif cell == 1:
            # Black
            ant.turn_left()
            board[ant.coordinates.y][ant.coordinates.x] = 0
            ant.move_forward()


# Rendering
def render(board):
    y = len(board)
    x = len(board[1])
    for a in range(0, x + 2):
        if a != x + 1:
            print("-", end="")
        else:
            print("-")
    for i in range(0, y):
        print("|", end="")
        for j in range(0, x):
            if board[i][j] == 1:
                print("#", end="")
            else:
                print(" ", end="")
        print("|")
    for a in range(0, x + 2):
        if a != x + 1:
            print("-", end="")
        else:
            print("-")


# LOOP
def langtons_ant(board, ant, wait):
    while True:
        os.system("cls")
        render(board)
        ant_move(board, ant)
        time.sleep(wait)


if __name__ == "__main__":
    board = init_board(int(sys.argv[1]), int(sys.argv[2]))
    position = get_random_point(board)
    myAnt = Ant(position[0], position[1])
    langtons_ant(board, myAnt, int(sys.argv[3]))
