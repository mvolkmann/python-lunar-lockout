from itertools import permutations
import sys
from typing import List, Tuple

Permutation = Tuple[int, ...]
Permutations = List[Permutation]

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
COLORS = ['R', 'O', 'Y', 'G', 'B', 'P']
SIZE = len(BOARD_HEIGHTS)

# There are 720 of these which is SIZE factorial.
# We can only iterate over an iterator once.
# Realizing this as a list enables iterating over multiple times.
size_permutations: Permutations = list(permutations(range(1, SIZE + 1)))

def print_board(perms: Permutations) -> None:
    for row, perm in enumerate(perms):
        board_row = BOARD_HEIGHTS[row]
        s = ''
        for column in range(SIZE):
            index = perm[column]
            color = COLORS[index - 1]
            height = board_row[column]
            s += color + height + ' '
        print(s)

def solution(perms: Permutations) -> bool:
    # Verify that there are no duplicate colors in any column.
    for column in range(SIZE):
        color_indexes = set()
        for perm in perms:
            color_indexes.add(perm[column])
        if len(color_indexes) != len(perms):
            return False

    # Verify that all the pieces are unique.
    pieces = set()
    for row, perm in enumerate(perms):
        board_row = BOARD_HEIGHTS[row]
        for column in range(SIZE):
            index = perm[column]
            color = COLORS[index - 1]
            height = board_row[column]
            # print(row, column, color, height)
            pieces.add(color + height)
    return len(pieces) == len(perms) * SIZE

for p1 in size_permutations:
    for p2 in size_permutations:
        if not solution([p1, p2]):
            continue
        for p3 in size_permutations:
            if not solution([p1, p2, p3]):
                continue
            for p4 in size_permutations:
                if not solution([p1, p2, p3, p4]):
                    continue
                for p5 in size_permutations:
                    if not solution([p1, p2, p3, p4, p5]):
                        continue
                    for p6 in size_permutations:
                        ps = [p1, p2, p3, p4, p5, p6]
                        if solution(ps):
                            print_board(ps)
                            sys.exit()
