import numpy as np
import os
from random import randrange as rand

UP, DOWN, RIGHT, LEFT = (0, -1), (0, 1), (1, 0), (-1, 0)
class Apple:
    def __init__(self, w, h, position):
        while True:
            pos = (rand(w), rand(h))
            if pos not in position:
                self.position = pos
                break
                
class Snake:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def take_step(self):
        self.position = self.position[1:]
        self.position.append((self.position[-1][0] + self.direction[0], self.position[-1][1] + self.direction[1]))

    def set_direction(self, direction):
        self.direction = direction

    def head(self):
        return self.position[-1]

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake([(2, 3), (3, 3), (4, 3)], RIGHT)
        self.apple = Apple(width, height, self.snake.position)
        self.score = 0

    def board_matrix(self, snake, apple):
        board = np.arange(self.height * self.width).reshape(self.height, self.width)
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) == snake.position[-1]:
                    board[i][j] = 2
                elif (j, i) in snake.position:
                    board[i][j] = 1
                elif (j, i) == apple.position:
                    board[i][j] = -1
                else:
                    board[i][j] = 0
        return board

    def render(self):
        board = self.board_matrix(self.snake, self.apple)
        print("+" + "-" * self.width + "+")
        for i in range(0, self.height):
            print("|", end='')
            for j in range(0, self.width):
                if board[i][j] == 0:
                    print(" ", end="")
                elif board[i][j] == 1:
                    print("o", end="")
                elif board[i][j] == 2:
                    print(":", end="")
                elif board[i][j] == -1:
                    print("*", end="")
            print('|')
        print("+" + "-" * self.width + "+")

    def move(self):
        new_direction = input()
        if new_direction == "":
            pass
        elif (new_direction == "w" or new_direction == "W") and self.snake.direction != DOWN:
            self.snake.set_direction(UP)
        elif (new_direction == "d" or new_direction == "D") and self.snake.direction != LEFT:
            self.snake.set_direction(RIGHT)
        elif (new_direction == "a" or new_direction == "A") and self.snake.direction != RIGHT:
            self.snake.set_direction(LEFT)
        elif (new_direction == "s" or new_direction == "S") and self.snake.direction != UP:
            self.snake.set_direction(DOWN)
        self.snake.take_step()

    def eat(self, direction):
        self.score += 1
        if direction == UP:
            self.snake.position.insert(0, (self.snake.position[0][0] + DOWN[0], self.snake.position[0][1] + DOWN[1]))
        elif direction == DOWN:
            self.snake.position.insert(0, (self.snake.position[0][0] + UP[0], self.snake.position[0][1] + UP[1]))
        elif direction == LEFT:
            self.snake.position.insert(0, (self.snake.position[0][0] + RIGHT[0], self.snake.position[0][1] + RIGHT[1]))
        else:
            self.snake.position.insert(0, (self.snake.position[0][0] + LEFT[0], self.snake.position[0][1] + LEFT[1]))

    def check_body_overlap(self, head):
        return True if head in self.snake.position[:-1] else False

    def check_border_overlap(self, head):
        return True if head[0] < 0 or head[1] < 0 or head[0] >= self.width or head[1] >= self.height else False

    def check_apple(self, head):
        return True if head == self.apple.position else False

def game_of_snake(w, h):
    game = Game(w, h)
    while True:
        os.system("cls")
        game.render()
        print(game.score)
        game.move()
        head = game.snake.head()
        if game.check_body_overlap(head) or game.check_border_overlap(head):
            print("Game Over! Your score is " + str(game.score))
            break
        elif game.check_apple(head):
            game.apple = Apple(w, h, game.snake.position)
            game.eat(game.snake.position)

if __name__ == "__main__":
    game_of_snake(25, 10)
    
