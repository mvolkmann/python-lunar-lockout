import csv
import math
from typing import Dict, List, Optional, Tuple

Action = Tuple[int, str]  # robot index and direction
Position = Tuple[int, int]  # column and row one-based indexes
State = List[Position]  # list of robot positions

DEBUG = False
SIZE = 5
CENTER = math.ceil(SIZE / 2)
TARGET = '#'

# Order of robots in State is same as order of robot_ids.
robot_ids = ('R', 'O', 'Y', 'G', 'B', 'P')
robot_names = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')

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
                    robots = [
                        _make_position(coords[0], coords[1]),  # red
                        _make_position(coords[2], coords[3]),  # orange
                        _make_position(coords[4], coords[5]),  # yellow
                        _make_position(coords[6], coords[7]),  # green
                        _make_position(coords[8], coords[9]),  # blue
                        _make_position(coords[10], coords[11])  # purple
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
        # print('.', end='') # print a dot for each action attempted

        robot_index, direction = action

        if DEBUG:
            print('moving', robot_names[robot_index], direction_map[direction])

        column, row = robots[robot_index]

        # Find the closest robot that will block the move.
        blocker: Optional[Position] = None
        # Avoid the false positive error about
        # blocker being an unsubscriptable object.
        # pylint: disable=E1136
        for index, position in enumerate(robots):
            if index == robot_index:
                continue
            c, r = position

            if direction == 'U' and c == column and r < row - 1:
                if blocker is None or r > blocker[1]:
                    blocker = position
            elif direction == 'D' and c == column and r > row + 1:
                if blocker is None or r < blocker[1]:
                    blocker = position
            elif direction == 'L' and r == row and c < column - 1:
                if blocker is None or c > blocker[0]:
                    blocker = position
            elif direction == 'R' and r == row and c > column + 1:
                if blocker is None or c < blocker[0]:
                    blocker = position

        if blocker is None:
            raise ValueError('invalid move')

        new_robots = robots.copy()
        c, r = blocker
        dx, dy = direction_deltas[direction]
        new_robots[robot_index] = (c - dx, r - dy)
        return new_robots
