from itertools import permutations
import sys
from typing import List, Set, Tuple

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

def log(perms: Permutations, text: str) -> None:
    if len(perms) == 6:
        print(text)

def print_board(perms: Permutations) -> None:
    if len(perms) < 6:
        return
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
    log(perms, '\nEvaluating:')
    print_board(perms)

    # Verify that there are no duplicate colors in any column.
    color_numbers: Set[int] = set()
    for column in range(SIZE):
        for perm in perms:
            color_number = perm[column]
            if color_number in color_numbers:
                log(perms,
                    f'duplicated color {COLORS[color_number - 1]} in column {column + 1}')
                return False
            color_numbers.add(color_number)
        color_numbers.clear()

    # Verify that all the pieces are unique.
    pieces: Set[str] = set()
    for row, perm in enumerate(perms):
        board_row = BOARD_HEIGHTS[row]
        for column in range(SIZE):
            color = COLORS[perm[column] - 1]
            height = board_row[column]
            # print(row, column, color, height)
            piece = color + height
            if piece in pieces:
                log(perms, f'duplicated piece {piece}')
                return False
            pieces.add(piece)
    return True

# There is no reason to evaluate any permutation
# other than the first for p1.
p1 = size_permutations[0]
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
                ps = [p1, p2, p3, p4, p5]
                if not solution(ps):
                    continue
                # print_board(ps)
                # sys.exit()
                for p6 in size_permutations:
                    ps = [p1, p2, p3, p4, p5, p6]
                    if solution(ps):
                        print('\nSolution:')
                        print_board(ps)
                        sys.exit()

print('no solution found')
