# global-statement: Using the global statement
# pylint: disable=W0603

import csv
import math
#import sys
from typing import Any, Dict, List, Tuple

# sys.setrecursionlimit(50000)

DEBUG = False
SIZE = 5
CENTER = math.floor(SIZE / 2)
TARGET = '#'

Action = Tuple[int, str]  # robot index and direction
Position = Tuple[int, int]  # column and row zero-based indexes
robot_ids = ('R', 'O', 'Y', 'G', 'B', 'P')
robot_names = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
# Order of robots in list is same as order of robot_ids.
Robots = List[Position]

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

robots_seen = set()
solved = False

def can_move(robots: Robots, robot_index: int, direction: str) -> bool:
    # validate_direction(direction)

    log('\ngame.py can_move: robots =', robots)
    log('game.py can_move: robot_index =', robot_index)
    log('game.py can_move: direction =', direction)

    column, row = robots[robot_index]

    can = False
    for index, position in enumerate(robots):
        if index == robot_index:
            continue
        c, r = position

        adjacent: bool = \
            (direction == 'U' and c == column and r == row - 1) or \
            (direction == 'D' and c == column and r == row + 1) or \
            (direction == 'L' and r == row and c == column - 1) or \
            (direction == 'R' and r == row and c == column + 1)
        if adjacent:
            # print('game.py can_move: adjacent')
            return False

        blocks: bool = \
            (direction == 'U' and c == column and r < row - 1) or \
            (direction == 'D' and c == column and r > row + 1) or \
            (direction == 'L' and r == row and c < column - 1) or \
            (direction == 'R' and r == row and c > column + 1)
        if blocks:
            can = True

    # print('game.py can_move: can =', can)
    return can

def get_cell(robots: Robots, column: int, row: int) -> str:
    for index, position in enumerate(robots):
        c, r = position
        if c == column and r == row:
            return robot_ids[index]
    is_center = column == CENTER and row == CENTER
    return '#' if is_center else ' '

def get_possible_actions(robots: Robots) -> List[Action]:
    actions = []
    for robot_index in range(len(robots)):
        for direction in directions:
            if can_move(robots, robot_index, direction):
                actions.append((robot_index, direction))
    return actions

def have_seen(robots: Robots) -> bool:
    global robots_seen
    key = to_string(robots)
    seen = key in robots_seen
    if not seen:
        robots_seen.add(key)
    return seen

def is_solved(robots: Robots) -> bool:
    column, row = robots[0]  # red robot
    return column == CENTER and row == CENTER

def load_puzzles(file_path: str) -> Dict[int, Robots]:
    puzzles = {}
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            number, rx, ry, ox, oy, yx, yy, gx, gy, bx, by, px, py = row
            robots = [
                make_position(rx, ry),  # red
                make_position(ox, oy),  # orange
                make_position(yx, yy),  # yellow
                make_position(gx, gy),  # green
                make_position(bx, by),  # blue
                make_position(px, py)  # purple
            ]
            puzzles[int(number)] = robots
    return puzzles

def log(*args: Any) -> None:
    if DEBUG:
        print(*args)

def make_position(x: str, y: str) -> Position:
    return (int(x) - 1, int(y) - 1)

def print_action(label: str, action: Action) -> None:
    index, direction = action
    print(label, robot_names[index], direction_map[direction])

def print_actions(label: str, actions: List[Action]) -> None:
    print(label)
    for action in actions:
        print_action('  ', action)

def print_board(robots: Robots) -> None:
    log(to_string(robots))
    border = '+---' * SIZE + '+'
    for row in range(SIZE):
        print(border)
        s = '|'
        for column in range(SIZE):
            s += ' ' + get_cell(robots, column, row) + ' |'
        print(s)
    print(border)

def solve(robots: Robots, solution: List[Action] = [], depth: int = 0) -> None:
    global solved

    if have_seen(robots):
        return

    if is_solved(robots):
        solved = True  # prevents further actions
        print_actions('\nSolution:', solution)
        return

    actions = get_possible_actions(robots)

    if len(actions) == 0:
        log('no more actions')
        return

    if DEBUG:
        print_actions('\nActions:', actions)

    for action in actions:
        if solved:
            return
        log('depth =', str(depth))
        if DEBUG:
            print_board(robots)
        new_robots = take_action(action, robots)
        solve(new_robots, [*solution, action], depth + 1)  # recursive call

def take_action(action: Action, robots: Robots) -> Robots:
    #print('.', end='')

    robot_index, direction = action
    # validate_direction(direction)

    log('moving', robot_names[robot_index], direction_map[direction])

    column, row = robots[robot_index]

    # Find the CLOSEST robot that will block the move.
    blocker = None
    for index, position in enumerate(robots):
        if index == robot_index:
            continue
        c, r = position

        if direction == 'U' and c == column and r < row - 1:
            if not blocker or r > blocker[1]:
                blocker = position
        elif direction == 'D' and c == column and r > row + 1:
            if not blocker or r < blocker[1]:
                blocker = position
        elif direction == 'L' and r == row and c < column - 1:
            if not blocker or c > blocker[0]:
                blocker = position
        elif direction == 'R' and r == row and c > column + 1:
            if not blocker or c < blocker[0]:
                blocker = position

    if not blocker:
        raise ValueError('invalid move')

    new_robots = robots.copy()
    #c, r = blocker
    c = blocker[0]
    r = blocker[1]
    if direction == 'U':
        new_robots[robot_index] = (c, r + 1)
    elif direction == 'D':
        new_robots[robot_index] = (c, r - 1)
    elif direction == 'L':
        new_robots[robot_index] = (c + 1, r)
    elif direction == 'R':
        new_robots[robot_index] = (c - 1, r)
    return new_robots

def to_string(robots: Robots) -> str:
    return ''.join(map(lambda pos: f'{pos[0]}{pos[1]}', robots))

def valid_cell(column: int, row: int) -> bool:
    return 0 <= column < SIZE and 0 <= row < SIZE

# def validate_direction(direction: str) -> None:
#     if not direction in directions:
#         raise ValueError('invalid direction ' + direction)

puzzles = load_puzzles('puzzles.csv')

for game in range(len(puzzles)):
    robots = puzzles[game + 1]
    print('\nGame #' + str(game + 1))
    print_board(robots)
    solved = False
    robots_seen = set()
    solve(robots)

# Solve a single puzzle instead of all.
# robots = puzzles[9]
# print_board(robots)
# solve(robots)
