# global-statement: Using the global statement
# pylint: disable=W0603

import math
from typing import List, Tuple

SIZE = 5
CENTER = math.floor(SIZE / 2)
TARGET = '#'

Action = Tuple[int, str]  # robot index and direction
Position = Tuple[int, int]  # column and row indexes
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

# List of robot data which includes the
# zero-based column and row of each robot.
robots: Robots = [
    (4, 4),
    (3, 0),
    (1, 4),
    (1, 1),
    (-1, -1),
    (3, 3)
]

solved = False

def can_move(robot_index: int, direction: str, robots: Robots) -> bool:
    validate_direction(direction)
    column, row = robots[robot_index]

    for index, position in enumerate(robots):
        if index == robot_index:
            continue
        c, r = position

        blocks: bool = \
            (direction == 'U' and c == column and r < row - 1) or \
            (direction == 'D' and c == column and r > row + 1) or \
            (direction == 'L' and r == row and c < column - 1) or \
            (direction == 'R' and r == row and c > column + 1)
        if blocks:
            return True

    return False

def get_cell(robots: Robots, column: int, row: int):
    for index, position in enumerate(robots):
        c, r = position
        if c == column and r == row:
            return robot_ids[index]
    is_center = column == CENTER and row == CENTER
    return '#' if is_center else ' '

def get_possible_actions(robots: Robots) -> List[Action]:
    """Get all possible actions."""
    actions = []
    for robot_index in range(len(robots)):
        for direction in directions:
            if can_move(robot_index, direction, robots):
                actions.append((robot_index, direction))
    return actions

def print_action(label: str, action: Action) -> None:
    index, direction = action
    print(label, robot_names[index], direction_map[direction])

def print_actions(actions: List[Action]) -> None:
    print('Actions:')
    for action in actions:
        print_action('  ', action)

def print_board(robots: Robots) -> None:
    border = '+---' * SIZE + '+'
    for row in range(SIZE):
        print(border)
        s = '|'
        for column in range(SIZE):
            s += ' ' + get_cell(robots, column, row) + ' |'
        print(s)
    print(border)

def solve(robots: Robots, depth: int = 0) -> None:
    global solved

    print_board(robots)
    if is_solved(robots):
        solved = True  # prevents further actions
        print('Solved!')
        return

    actions = get_possible_actions(robots)
    if len(actions) == 0:
        return

    for action in actions:
        if solved:
            return
        new_robots = take_action(action, robots)
        solve(new_robots, depth + 1)  # recursive call

def is_solved(robots: Robots) -> bool:
    column, row = robots[0]  # red robot
    return column == CENTER and row == CENTER

def take_action(action: Action, robots: Robots) -> Robots:
    robot_index, direction = action
    validate_direction(direction)

    robot_name = robot_names[robot_index]
    print('moving', robot_name, 'robot', direction_map[direction])
    column, row = robots[robot_index]

    # Find the robot that will block the move.
    blocker = None
    for index, position in enumerate(robots):
        if index == robot_index:
            continue
        c, r = position

        if direction == 'U' and c == column and r < row - 1:
            if not blocker or c > blocker[0]:
                blocker = position
        elif direction == 'D' and c == column and r > row + 1:
            if not blocker or c < blocker[0]:
                blocker = position
        elif direction == 'L' and r == row and c < column - 1:
            if not blocker or r > blocker[0]:
                blocker = position
        elif direction == 'R' and r == row and c > column - 1:
            if not blocker or r < blocker[0]:
                blocker = position

    if not blocker:
        raise ValueError('invalid move')

    new_robots = robots.copy()
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

def valid_cell(column: int, row: int) -> bool:
    return 0 <= column < SIZE and 0 <= row < SIZE

def validate_direction(direction: str) -> None:
    if not direction in directions:
        raise ValueError('invalid direction ' + direction)

solve(robots)
