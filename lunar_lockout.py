import csv
import math
from typing import Dict, List, Tuple
from util import log

DEBUG = False
SIZE = 5
CENTER = math.ceil(SIZE / 2)
TARGET = '#'

Action = Tuple[int, str]  # robot index and direction
Position = Tuple[int, int]  # column and row one-based indexes
robot_ids = ('R', 'O', 'Y', 'G', 'B', 'P')
robot_names = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
# Order of robots in list is same as order of robot_ids.
State = List[Position]  # list of robot positions

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

def _can_move(robots: State, robot_index: int, direction: str) -> bool:
    # validate_direction(direction)
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

def _get_cell(robots: State, column: int, row: int) -> str:
    for index, position in enumerate(robots):
        c, r = position
        if c == column and r == row:
            return robot_ids[index]
    is_center = column == CENTER and row == CENTER
    return '#' if is_center else ' '

def _make_position(x: str, y: str) -> Position:
    return (int(x), int(y))

def _print_action(label: str, action: Action) -> None:
    index, direction = action
    print(label, robot_names[index], direction_map[direction])

class LunarLockout:
    @staticmethod
    def get_possible_actions(robots: State) -> List[Action]:
        actions = []
        for robot_index in range(len(robots)):
            for direction in directions:
                if _can_move(robots, robot_index, direction):
                    actions.append((robot_index, direction))
        return actions

    @staticmethod
    def is_solved(robots: State) -> bool:
        column, row = robots[0]  # red robot
        return column == CENTER and row == CENTER

    @staticmethod
    def load_puzzles(file_path: str) -> Dict[int, State]:
        puzzles = {}
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                number, coords = row
                if not number.startswith('#'):
                    rx, ry, ox, oy, yx, yy, gx, gy, bx, by, px, py = coords
                    robots = [
                        _make_position(rx, ry),  # red
                        _make_position(ox, oy),  # orange
                        _make_position(yx, yy),  # yellow
                        _make_position(gx, gy),  # green
                        _make_position(bx, by),  # blue
                        _make_position(px, py)  # purple
                    ]
                    puzzles[int(number)] = robots
        return puzzles

    @staticmethod
    def print_actions(label: str, actions: List[Action]) -> None:
        print(label)
        for action in actions:
            _print_action('  ', action)

    @staticmethod
    def print_state(robots: State) -> None:
        border = '+---' * SIZE + '+'
        for row in range(1, SIZE + 1):
            print(border)
            s = '|'
            for column in range(1, SIZE + 1):
                s += ' ' + _get_cell(robots, column, row) + ' |'
            print(s)
        print(border)

    @staticmethod
    def state_string(robots: State) -> str:
        return ''.join(map(lambda pos: f'{pos[0]}{pos[1]}', robots))

    @staticmethod
    def take_action(action: Action, robots: State) -> State:
        #print('.', end='')

        robot_index, direction = action
        # validate_direction(direction)

        log(DEBUG, 'moving',
            robot_names[robot_index], direction_map[direction])

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
