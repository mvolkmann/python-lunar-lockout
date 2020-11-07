import csv
from typing import Dict, List, Tuple

Action = Tuple[str, str]  # piece id and direction
Position = Tuple[int, int]  # column and row one-based indexes
State = Dict[str, Position]  # keys are piece ids and values are positions

COLUMNS = 5
ROWS = 4

# Order of pieces in State is same as order of piece_ids.
piece_ids = list('ABCDEFGHJ')

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

piece_sizes = {
    'A': (2, 2),
    'B': (1, 1),
    'C': (1, 1),
    'D': (2, 1),
    'E': (2, 1),
    'F': (1, 2),
    'G': (1, 2),
    'H': (1, 2),
    'J': (1, 2)
}

# def _can_move(state: State, piece_index: int, direction: str) -> bool:
#     """Determine whether a piece can move in a direction in a given State."""
#     column, row = pieces[piece_index]

#     can = False
#     for index, position in enumerate(pieces):
#         if index == piece_index:
#             continue
#         c, r = position

#         adjacent: bool = \
#             (direction == 'U' and c == column and r == row - 1) or \
#             (direction == 'D' and c == column and r == row + 1) or \
#             (direction == 'L' and r == row and c == column - 1) or \
#             (direction == 'R' and r == row and c == column + 1)
#         if adjacent:
#             return False

#         blocks: bool = \
#             (direction == 'U' and c == column and r < row - 1) or \
#             (direction == 'D' and c == column and r > row + 1) or \
#             (direction == 'L' and r == row and c < column - 1) or \
#             (direction == 'R' and r == row and c > column + 1)
#         if blocks:
#             can = True

#     # print('game.py can_move: can =', can)
#     return can


# def _get_cell(pieces: State, column: int, row: int) -> str:
#     """Get the character to print for a given board cell."""
#     for index, position in enumerate(pieces):
#         c, r = position
#         if c == column and r == row:
#             return piece_ids[index]
#     is_center = column == row == CENTER
#     return '#' if is_center else ' '


# def _make_position(x: str, y: str) -> Position:
#     """Create a Position from x and y string values."""
#     return (int(x), int(y))


class MovingPieces:
    @staticmethod
    def action_string(action: Action) -> str:
        """Get string representation of an Action."""
        piece_id, direction = action
        return piece_id + ' ' + direction_map[direction]

    @staticmethod
    def get_possible_actions(pieces: State) -> List[Action]:
        """Get all the possible actions that can be taken in a given State."""
        actions = []
        # for piece_index in range(len(pieces)):
        #     for direction in directions:
        #         if _can_move(pieces, piece_index, direction):
        #             actions.append((piece_index, direction))
        return actions

    @staticmethod
    def initialize() -> None:
        pass

    @staticmethod
    def is_solved(state: State) -> bool:
        """Determine if a State represents a solved puzzle."""
        return state['A'] == (3, 1) and state['D'] == (1, 1) and state['E'] == (1, 2)

    @staticmethod
    def load_puzzles() -> Dict[int, State]:
        """Load a set of puzzles from a file."""
        puzzles = {}
        with open('moving_pieces.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                number, coords = row
                if not number.startswith('#'):
                    state = {}
                    for i in range(len(piece_ids)):
                        piece_id = piece_ids[i]
                        ci = i * 2
                        state[piece_id] = (
                            int(coords[ci]), int(coords[ci + 1]))
                    puzzles[int(number)] = state
        return puzzles

    @ staticmethod
    def print_actions(label: str, actions: List[Action]) -> None:
        """Print a list of Actions."""
        print(label)
        for action in actions:
            print('  ', MovingPieces.action_string(action))

    @ staticmethod
    def print_state(state: State) -> None:
        """Print a State."""
        board = [[' '] * 5 for _ in range(4)]

        for piece_id, position in state.items():
            column, row = position
            width, height = piece_sizes[piece_id]
            for c in range(width):
                for r in range(height):
                    board[row - 1 + r][column - 1 + c] = piece_id

        border = '+---' * 5 + '+'
        for row in range(4):
            print(border)
            print('| ' + ' | '.join(board[row]) + ' |')
        print(border)

    @ staticmethod
    def state_string(pieces: State) -> str:
        """Get the string representation of a State."""
        return ''.join(map(lambda pos: f'{pos[0]}{pos[1]}', pieces))

    @ staticmethod
    def take_action(state: State, action: Action) -> State:
        """Take an Action on a State and return a new State."""
        # print('.', end='')  # print a dot for each action attempted

        return state
