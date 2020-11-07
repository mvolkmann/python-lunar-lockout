# It sucks that this puzzle has two trick tower positions
# and two trick pieces.
# The Y5 piece must go on a tower that seems to need a 6 piece and
# the O6 piece must go on a tower that seems to need a 5 piece.
# Many hours of my life were wasted until I found this website:
# https://daniel.hepper.net/blog/2010/01/how-to-solve-the-36-cube-puzzle/
from itertools import permutations
import sys
from typing import List, Set, Tuple

Permutation = Tuple[int, ...]
Permutations = List[Permutation]

# These numbers represent the size of the piece
# that will fit at each board position.
BOARD_HEIGHTS = [
    '532146',
    '415253',  # 3rd column looks like 6, but acts like 5.
    '653412',
    '126364',  # 3rd column looks like 5, but acts like 6.
    '241635',
    '364521'
]

# This color order allows the special Y5 and O6 pieces
# to be placed on the two special positions.
COLORS = ['P', 'Y', 'B', 'O', 'R', 'G']
SIZE = len(BOARD_HEIGHTS)


def log(perms: Permutations, text: str) -> None:
    if len(perms) == 6:
        print(text)


def print_board(perms: Permutations) -> None:
    if len(perms) < 6:
        return
    print()
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
    # log(perms, '\nEvaluating:')
    # print_board(perms)

    # Check for duplicate colors in any column.
    color_numbers: Set[int] = set()
    for column in range(SIZE):
        for perm in perms:
            color_number = perm[column]
            if color_number in color_numbers:
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
            piece = color + height
            if piece in pieces:
                # log(perms, f'duplicated piece {piece}')
                return False
            pieces.add(piece)
    return True


def keep_perm(perm: Permutation) -> bool:
    return all(map(lambda t: t[1] != t[0] + 1, enumerate(perm)))


# There are 720 of these which is SIZE factorial.
# We can only iterate over an iterator once.
# Realizing this as a list enables iterating over multiple times.
size_permutations: Permutations = list(permutations(range(1, SIZE + 1)))

# There is no reason to evaluate any permutation
# other than the first for p1.
p1 = size_permutations.pop(0)

size_permutations = list(filter(keep_perm, size_permutations))
print('filtered permutations =', len(size_permutations))

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
                        print('\nSolution:')
                        print_board(ps)
                        sys.exit()

print('\nno solution found'.upper())
