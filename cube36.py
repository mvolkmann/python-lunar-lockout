from itertools import permutations
#import sys
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

def is_solution(perms: Permutations) -> bool:
    pieces = set()
    for row, pick in enumerate(perms):
        board_row = BOARD_HEIGHTS[row]
        for column in range(SIZE):
            index = pick[column]
            color = COLORS[index - 1]
            height = board_row[column]
            pieces.add(color + height)
    return len(pieces) == SIZE * SIZE

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

def unique(perm: Permutation):
    for other_perm in perms:
        for i in range(SIZE):
            if other_perm[i] == perm[i]:
                return False
    return True

# Pick the first SIZE of these with no column duplications.
perms: Permutations = []
for i in range(SIZE):
    for perm in size_permutations:
        if unique(perm):
            perms.append(perm)
            break
print('cube36.py x: perms =', perms)
print('is solution?', is_solution(perms))
print_board(perms)
