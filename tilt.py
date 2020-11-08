import csv
import math
from typing import Dict, List, Optional, Tuple
from share import direction_map, directions

Action = str  # direction letter
# The outer list holds rows described by inner lists.
# This means the indexes are board[row][column]
Board = List[List[str]]
Position = List[int]  # column and row one-based indexes
Piece = Tuple[str, Position]
State = Board

DEBUG = False
SIZE = 5
CENTER = math.floor(SIZE / 2)
TARGET = 'O'

#directions = cast(List[Action], direction_map.keys())


def _place_pieces(board: State, name: str, coords: str) -> List[Position]:
    """Set the positions for a single kind of piece."""
    i = 0
    length = len(coords)
    positions: List[Position] = []
    while i < length:
        column = int(coords[i])
        row = int(coords[i + 1])
        board[row - 1][column - 1] = name
        i += 2
    return positions


class Tilt:
    last_direction: Optional[Action] = None

    @staticmethod
    def action_string(action: Action) -> str:
        """Get string representation of an Action."""
        return 'tilt ' + direction_map[action]

    @staticmethod
    def get_possible_actions(_: State) -> List[Action]:
        """Get all the possible actions that can be taken in a given State."""
        return list(filter(lambda d: d != Tilt.last_direction, directions))

    @staticmethod
    def initialize() -> None:
        Tilt.last_direction = None

    @staticmethod
    def is_solved(board: State) -> bool:
        """Determine if a State represents a solved puzzle."""
        # Are there no green pieces left?
        for row in range(SIZE):
            if 'G' in board[row]:
                return False
        return True

    @staticmethod
    def load_puzzles() -> Dict[int, State]:
        """Load a set of puzzles from a file."""
        puzzles = {}
        with open('tilt.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                number, blockers, greens, blues = row
                if not number.startswith('#'):
                    # Build a SIZE x SIZE array of pieces.
                    board = []
                    for _ in range(SIZE):
                        board.append([' '] * SIZE)
                    board[CENTER][CENTER] = TARGET
                    _place_pieces(board, 'X', blockers)
                    _place_pieces(board, 'G', greens)
                    _place_pieces(board, 'B', blues)
                    puzzles[int(number)] = board
        return puzzles

    @staticmethod
    def print_actions(label: str, actions: List[Action]) -> None:
        """Print a list of Actions."""
        print(label)
        for action in actions:
            print('  ', Tilt.action_string(action))

    @staticmethod
    def print_state(board: State) -> None:
        """Print a State."""
        border = '+---' * SIZE + '+'
        for row in range(SIZE):
            print(border)
            s = '|'
            row_list = board[row]
            for column in range(SIZE):
                s += ' ' + row_list[column] + ' |'
            print(s)
        print(border)

    @staticmethod
    def state_string(board: State) -> str:
        """Get the string representation of a State."""
        return str(board)

    @staticmethod
    def take_action(board: State, direction: Action) -> State:
        """Take an Action on a State and return a new State."""

        # Make a deep copy of the state.
        new_board = []
        for row in range(SIZE):
            new_board.append(board[row].copy())

        forward = direction in ('R', 'D')
        horizontal = direction in ('L', 'R')

        for index in range(SIZE):
            # Create a vector of the pieces being considered
            # where moves are from right to left.
            vector = []
            if horizontal:
                row = index
                vector = new_board[row]
            else:
                column = index
                for row in range(SIZE):
                    vector.append(new_board[row][column])
            if forward:
                vector.reverse()

            valid = Tilt._process_vector(vector, direction)
            if not valid:
                return board

            # Copy the vector to the new board
            if forward:
                vector.reverse()
            if horizontal:
                row = index
                new_board[row] = vector
            else:
                column = index
                for row in range(SIZE):
                    new_board[row][column] = vector[row]

        return new_board

    @staticmethod
    def _process_vector(vector: List[str], direction: str) -> bool:
        has_hole = TARGET in vector

        # Move the pieces in the vector to the left.
        target = 0
        for index in range(SIZE):
            piece = vector[index]
            is_blue = piece == 'B'
            is_green = piece == 'G'
            # if index > target and (is_blue or is_green):
            if is_blue or is_green:
                vector[index] = ' '
                in_hole = has_hole and target <= CENTER < index
                if not in_hole:
                    vector[target] = piece
                    target += 1
                    Tilt.last_direction = direction
                elif is_blue:  # not valid for blue to go in hole
                    return False
            elif piece == 'X':
                target = index + 1
        return True
