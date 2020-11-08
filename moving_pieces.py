import csv
import sys
from typing import Dict, List, Tuple
from share import direction_map, directions

Action = Tuple[str, str]  # piece id and direction
Board = List[List[str]]  # outer array holds rows; inner arrays hold columns
Position = Tuple[int, int]  # column and row one-based indexes
State = Dict[str, Position]  # keys are piece ids and values are positions

COLUMNS = 5
ROWS = 4
SINGLE_PIECES = ['B', 'C']
VERTICAL_PIECES = ['F', 'G', 'H', 'J']

sys.setrecursionlimit(10**5)  # 10**4 is not enough

# Order of pieces in State is same as order of piece_ids.
piece_ids = list('ABCDEFGHJ')

piece_sizes = {
    'A': (2, 2),  # width, height
    'B': (1, 1),
    'C': (1, 1),
    'D': (2, 1),
    'E': (2, 1),
    'F': (1, 2),
    'G': (1, 2),
    'H': (1, 2),
    'J': (1, 2)
}


def _can_move(state: State, piece_id: str, direction: str) -> bool:
    """Determine whether a piece can move in a direction in a given State."""
    # Get the one or two cells that are the target of the move.
    target_cells: List[Position] = []

    column, row = state[piece_id]
    width, height = piece_sizes[piece_id]

    if direction == 'L' and column > 1:
        target_cells = [(column - 1, row + i)
                        for i in range(height)]
    elif direction == 'R' and column + width <= COLUMNS:
        target_cells = [(column + width, row + i)
                        for i in range(height)]
    elif direction == 'D' and row + height <= ROWS:
        target_cells = [(column + i, row + height)
                        for i in range(width)]
    elif direction == 'U' and row > 1:
        target_cells = [(column + i, row - 1)
                        for i in range(width)]

    if not target_cells:
        return False

    # Determine if the target cells are empty.
    return all(map(lambda cell: _is_empty(state, cell), target_cells))


def _get_board(state: State) -> Board:
    """Get the character to print for a given board cell."""
    board = [[' '] * COLUMNS for _ in range(ROWS)]
    for piece_id, position in state.items():
        column, row = position
        width, height = piece_sizes[piece_id]
        for c in range(width):
            for r in range(height):
                board[row - 1 + r][column - 1 + c] = piece_id
    return board


def _is_empty(state: State, cell: Position) -> bool:
    c, r = cell
    # If any piece occupies this cell then it is not empty.
    for piece_id, position in state.items():
        column, row = position
        width, height = piece_sizes[piece_id]
        if column <= c < column + width and row <= r < row + height:
            return False
    return True


class MovingPieces:
    @staticmethod
    def action_string(action: Action) -> str:
        """Get string representation of an Action."""
        piece_id, direction = action
        return piece_id + ' ' + direction_map[direction]

    @staticmethod
    def get_possible_actions(state: State) -> List[Action]:
        """Get all the possible actions that can be taken in a given State."""
        actions: List[Action] = []
        for piece_id, position in state.items():
            column, row = position
            width, height = piece_sizes[piece_id]
            for direction in directions:
                # Get the one or two cells that are the target of the move.
                target_cells: List[Position] = []

                if direction == 'L' and column > 1:
                    target_cells = [(column - 1, row + i)
                                    for i in range(height)]
                elif direction == 'R' and column + width <= COLUMNS:
                    target_cells = [(column + width, row + i)
                                    for i in range(height)]
                elif direction == 'D' and row + height <= ROWS:
                    target_cells = [(column + i, row + height)
                                    for i in range(width)]
                elif direction == 'U' and row > 1:
                    target_cells = [(column + i, row - 1)
                                    for i in range(width)]
                if not target_cells:
                    continue
                # If those cells are open ...
                if all(map(lambda cell: _is_empty(state, cell), target_cells)):
                    actions.append((piece_id, direction))
        return actions

    @staticmethod
    def initialize() -> None:
        pass

    @staticmethod
    def is_solved(state: State) -> bool:
        """Determine if a State represents a solved puzzle."""
        return state['A'] == (4, 1) and state['D'] == (1, 1) and state['E'] == (1, 2)

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
                    for i, piece_id in enumerate(piece_ids):
                        ci = i * 2
                        state[piece_id] = (
                            int(coords[ci]), int(coords[ci + 1]))
                    puzzles[int(number)] = state
        return puzzles

    @staticmethod
    def print_actions(label: str, actions: List[Action]) -> None:
        """Print a list of Actions."""

        print(label)

        skip_next = False
        step = 0
        end = len(actions) - 1
        for i, action in enumerate(actions):
            if skip_next:
                skip_next = False
                continue

            s = MovingPieces.action_string(action)
            skip_next = i < end and actions[i + 1] == action
            if skip_next:
                s += ' twice'

            step += 1
            print(f'  {step}) {s}')

    @staticmethod
    def print_state(state: State) -> None:
        """Print a State."""
        board = _get_board(state)
        border = '+---' * COLUMNS + '+'
        for row in range(ROWS):
            print(border)
            print('| ' + ' | '.join(board[row]) + ' |')
        print(border)

    @staticmethod
    def state_string(state: State) -> str:
        """Get the string representation of a State."""

        def position_string(piece_id: str) -> str:
            column, row = state[piece_id]
            return f'{column}{row}'

        s_positions: List[str] = list(map(position_string, SINGLE_PIECES))
        v_positions: List[str] = list(map(position_string, VERTICAL_PIECES))
        s_positions.sort()
        v_positions.sort()
        return position_string('A') \
            + position_string('D') \
            + position_string('E') \
            + ''.join(s_positions) \
            + ''.join(v_positions)

    @staticmethod
    def take_action(state: State, action: Action) -> State:
        """Take an Action on a State and return a new State."""
        # print('.', end='')  # print a dot for each action attempted

        new_state = state.copy()
        piece_id, direction = action

        if not _can_move(state, piece_id, direction):
            raise ValueError(
                'invalid move ' + MovingPieces.action_string(action))

        column, row = state[piece_id]
        if direction == 'L':
            new_state[piece_id] = (column - 1, row)
        elif direction == 'R':
            new_state[piece_id] = (column + 1, row)
        elif direction == 'U':
            new_state[piece_id] = (column, row - 1)
        elif direction == 'D':
            new_state[piece_id] = (column, row + 1)

        return new_state
