import csv
import math
import sys
from typing import Dict, List, Optional, Tuple

Action = str  # direction letter
Position = List[int]  # column and row one-based indexes
Piece = Tuple[str, Position]
# State keys are 'b' for blocker, 'g' for green, and 'b' for blue
# State values are piece positions as (column, row) tuples.
State = Dict[str, List[Position]]

DEBUG = False
SIZE = 5
CENTER = math.ceil(SIZE / 2)
TARGET = 'O'

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

last = None  # last direction moved

def _get_cell(state: State, column: int, row: int) -> str:
    """Get the character to print for a given board cell."""
    if column == row == CENTER:
        return 'O'
    for c, r in state['blockers']:
        if c == column and r == row:
            return 'X'
    for c, r in state['greens']:
        if c == column and r == row:
            return 'G'
    for c, r in state['blues']:
        if c == column and r == row:
            return 'B'
    return ' '

def _get_piece(state: State, column: int, row: int) -> Optional[Piece]:
    """Get the piece at a given board cell."""
    if column == row == CENTER:
        return None
    for position in state['blockers']:
        if position[0] == column and position[1] == row:
            return ('blocker', position)
    for position in state['greens']:
        if position[0] == column and position[1] == row:
            return ('green', position)
    for position in state['blues']:
        if position[0] == column and position[1] == row:
            return ('blue', position)
    return None

def _get_positions(coords: str) -> List[Position]:
    """Get the positions for a single kind of piece."""
    i = 0
    length = len(coords)
    positions = []
    while i < length:
        positions.append(_make_position(coords[i], coords[i + 1]))
        i += 2
    return positions

def _make_position(x: str, y: str) -> Position:
    """Create a Position from x and y string values."""
    return [int(x), int(y)]  # using list instead of tuple so its mutable

class Tilt:
    @staticmethod
    def action_string(action: Action) -> str:
        """Get string representation of an Action."""
        return direction_map[action]

    @staticmethod
    def get_possible_actions(state: State) -> List[Action]:
        """Get all the possible actions that can be taken in a given State."""
        return list(filter(lambda d: d != last, directions))

    @staticmethod
    def is_solved(state: State) -> bool:
        """Determine if a State represents a solved puzzle."""
        # Are there no green pieces left?
        return len(state['greens']) == 0

    @staticmethod
    def load_puzzles(file_path: str) -> Dict[int, State]:
        """Load a set of puzzles from a file."""
        puzzles = {}
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                number, blockers, greens, blues = row
                if not number.startswith('#'):
                    state = {}
                    state['blockers'] = _get_positions(blockers)
                    state['greens'] = _get_positions(greens)
                    state['blues'] = _get_positions(blues)
                    puzzles[int(number)] = state
        return puzzles

    @staticmethod
    def print_actions(label: str, actions: List[Action]) -> None:
        """Print a list of Actions."""
        print(label)
        for action in actions:
            print('  ', Tilt.action_string(action))

    @staticmethod
    def print_state(state: State) -> None:
        """Print a State."""
        border = '+---' * SIZE + '+'
        for row in range(1, SIZE + 1):
            print(border)
            s = '|'
            for column in range(1, SIZE + 1):
                s += ' ' + _get_cell(state, column, row) + ' |'
            print(s)
        print(border)

    @staticmethod
    def state_string(state: State) -> str:
        """Get the string representation of a State."""
        return str(state)

    @staticmethod
    def take_action(state: State, direction: Action) -> State:
        """Take an Action on a State and return a new State."""

        global last

        # print('.', end='')  # print a dot for each action attempted

        if DEBUG:
            print('tilting', direction_map[direction])

        new_state = state.copy()

        print('tilt.py take_action: direction =', direction)
        forward = direction == 'R' or direction == 'D'
        print('tilt.py take_action: forward =', forward)
        delta = -1 if forward else 1
        print('tilt.py take_action: delta =', delta)

        horizontal = direction == 'L' or direction == 'R'
        print('tilt.py take_action: horizontal =', horizontal)

        index = 0 if horizontal else 1
        print('tilt.py take_action: index =', index)

        start = SIZE if forward else 1
        print('tilt.py take_action: start =', start)
        stop = 1 if forward else SIZE
        print('tilt.py take_action: stop =', stop)

        for dim1 in range(1, SIZE + 1):
            print('tilt.py take_action: dim1 =', dim1)
            target = start
            # Find the first target cell in this row/column.
            for dim2 in range(start, stop, delta):
                print('tilt.py take_action: dim2 =', dim2)
                column = dim2 if horizontal else dim1
                row = dim1 if horizontal else dim2
                piece = _get_piece(state, column, row)
                print('looking for target, piece at', column, row, 'is', piece)
                if not piece:
                    target = column if horizontal else row
                    break

            print('tilt.py take_action: target =', target)

            for dim2 in range(start + delta, stop + delta, delta):
                if dim1 == dim2 == CENTER:
                    continue
                column = dim2 if horizontal else dim1
                row = dim1 if horizontal else dim2
                piece = _get_piece(state, column, row)
                print('piece at', column, row, 'is', piece)
                if piece:
                    if piece[0] == 'blocker':
                        target = column if horizontal else row
                    else:
                        # Move the piece to the target position.
                        # TODO: Handle falling through center hole.
                        position = piece[1]
                        position[index] = target
                        print('moved to', position)

                        # Remember the last successful move direction.
                        last = direction

                        # The target now becomes the space before this one.
                        target += delta

        print('tilt.py take_action: finished\n')
        return new_state
