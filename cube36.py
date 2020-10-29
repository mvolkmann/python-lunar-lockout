from itertools import permutations
from typing import Iterator, List, Tuple

Colors = List[str]
Board = List[Colors]
Sizes = Iterator[Tuple[int, ...]]  # returned by permutations

# These numbers represent the size of the piece
# that will fit at each board position.
BOARD_HEIGHTS = [
    '532146',
    '416253',
    '653412',
    '125364',
    '241635',
    '364521'
]

SIZE = len(BOARD_HEIGHTS)
COLORS = ['R', 'O', 'Y', 'G', 'B', 'P']
LENGTHS = range(1, SIZE + 1)
size_permutations: Sizes = permutations(range(1, SIZE + 1))

board = [[' '] * SIZE for _ in range(SIZE)]

def is_solution(board: Board) -> bool:
    for row in range(SIZE):
        board_row = board[row]
        if len(set(board_row)) != SIZE:
            return False
    return True

def print_board(board: Board) -> None:
    for row in range(SIZE):
        board_row = board[row]
        row_heights = BOARD_HEIGHTS[row]
        s = ''
        for column in range(SIZE):
            s += board_row[column] + row_heights[column] + ' '
        print(s)

for perm in size_permutations:
    print('cube36.py x: perm =', perm)
    color_map: Colors = list(map(lambda size: COLORS[size - 1], perm))
    for row in range(SIZE):
        board_row = board[row]
        row_heights = BOARD_HEIGHTS[row]
        for column in range(SIZE):
            height = int(row_heights[column])
            color = color_map[height - 1]
            board_row[column] = color
        board[row] = board_row
    if is_solution(board):
        print_board(board)
        break
