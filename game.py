import math
import random
# import sys
from typing import Dict, List, Optional, Tuple

# import matplotlib as mlp
# from matplotlib.pylab import rand
# import matplotlib.pyplot as plt
# import numpy as np

SIZE = 5
CENTER = math.floor(SIZE / 2)
TARGET = '#'

Action = Tuple[str, str] # letter and direction
Board = List[List[str]]
Position = Tuple[int, int]
Robots = Dict[str, Position]

# These are dx and dy values for directions.
direction_deltas = {
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1)
}
direction_map = {
    'D': 'down',
    'L': 'left',
    'R': 'right',
    'U': 'up'
}
directions = direction_map.keys()

# List of robot data which includes the
# letter, column, and row of each robot.
# Column and row are zero-based.
robots: Robots = {
    # 'R': (4, 4),
    # 'O': (4, 0),
    # 'Y': (3, 3),
    # 'G': (2, 1),
    # 'B': (-1, -1),
    # 'P': (1, 2)
    'R': (4, 4),
    'O': (3, 0),
    'Y': (1, 4),
    'G': (1, 1),
    'B': (-1, -1),
    'P': (3, 3)
}
letters = robots.keys()

def can_move(letter: str, direction: str) -> bool:
    validate_letter(letter)
    validate_direction(direction)
    column, row = robots[letter]
    dx, dy = direction_deltas[direction]
    c = column
    r = row
    distance = 0
    while True:
        c += dx
        r += dy
        if not valid_cell(c, r):  # off the board
            return False
        cell = board[r][c]
        if not cell in (' ', TARGET):  # hit another robot
            break
        distance += 1
    return distance > 0

# def draw_board():
#     plt.grid(True)
#     ax = plt.gca()  # get current axes

#     # Turn off x and y axis ticks and labels.
#     ax.axes.xaxis.set_visible(False)
#     ax.axes.yaxis.set_visible(False)

#     r = rand(SIZE, SIZE)
#     print('r =', r)
#     for row in range(SIZE):
#         for column in range(SIZE):
#             ax.add_patch(mlp.patches.Rectangle((column, row), 1, 1))
#     ax.imshow(r, interpolation='nearest')
#     plt.show()

def get_board(robots: Robots) -> Board:
    board = [[' '] * SIZE for _ in range(SIZE)]
    board[CENTER][CENTER] = TARGET

    for letter, position in robots.items():
        column, row = position
        if row >= 0 and column >= 0:
            board[row][column] = letter
    return board

def get_distance() -> float:
    """Get distance from red robot to target."""
    column, row = robots['R']
    return math.hypot(column - CENTER, row - CENTER)

def get_possible_actions() -> List[Action]:
    """Get all possible actions."""
    actions = []
    for letter in letters:
        for direction in directions:
            if can_move(letter, direction):
                actions.append((letter, direction))
    return actions

def get_random_action() -> Optional[Action]:
    actions = get_possible_actions()
    if len(actions) == 0:
        return None

    # Prefer to move R if possible.
    r_actions = filter(lambda a: a[0] == 'R', actions)
    first_r_action = next(r_actions, None)
    if first_r_action:
        return first_r_action

    return random.choice(actions)

def move_robot(letter: str, direction: str) -> None:
    validate_letter(letter)
    validate_direction(direction)
    print('moving robot', letter, direction_map[direction])
    column, row = robots[letter]
    begin_distance = get_distance()

    dx, dy = direction_deltas[direction]
    c = column
    r = row

    while True:
        c += dx
        r += dy
        if valid_cell(c, r):
            cell = board[r][c]
            if cell in (' ', TARGET):  # if not occupied
                # Vacate current cell.
                board[row][column] = ' '
                # Move to new cell.
                row = r
                column = c
                board[row][column] = letter
                robots[letter] = (column, row)
            else:
                print_board(board)
                if letter == 'R':
                    end_distance = get_distance()
                    # prefer moving red robot closer to target
                    reward = begin_distance - end_distance
                else:
                    reward = -1  # prefer to move red robot
                print('reward =', reward)
                break
        else:
            raise Exception('invalid move')

def print_board(board: Board) -> None:
    border = '+---' * SIZE + '+'
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def solved() -> bool:
    column, row = robots['R']
    return column == CENTER and row == CENTER

def valid_cell(column: int, row: int) -> bool:
    return 0 <= column < SIZE and 0 <= row < SIZE

def validate_direction(direction: str) -> None:
    if not direction in directions:
        raise ValueError('invalid direction ' + direction)

def validate_letter(letter: str) -> None:
    if not letter in letters:
        raise ValueError('invalid robot letter ' + letter)

board = get_board(robots)

# draw_board()
# sys.exit()

print_board(board)

# print(can_move('R', 'U'))
# print(can_move('R', 'D'))
# print(can_move('R', 'L'))
# print(can_move('R', 'R'))

# move_robot('R', 'U')
# move_robot('R', 'L')
# move_robot('R', 'D')
# move_robot('R', 'L')

# Solution
# move_robot('P', 'U')
# move_robot('G', 'R')
# move_robot('R', 'L')
# move_robot('R', 'U')
# if solved():
#     print('You win!')

while True:
    action = get_random_action()
    if action is None:
        print('Failed to find solution.')
        break
    move_robot(*action)
    if solved():
        print('Solution found!')
        break
