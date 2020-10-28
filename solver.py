# global-statement: Using the global statement
# pylint: disable=W0603

from typing import List, Set
from lunar_lockout import Action, LunarLockout as Game, State

DEBUG = False

def have_seen(state: State) -> bool:
    global states_seen
    key = Game.state_string(state)
    seen = key in states_seen
    if not seen:
        states_seen.add(key)
    return seen

def solve(state: State, solution: List[Action], depth: int = 0) -> None:
    global solved

    if have_seen(state):
        return

    if Game.is_solved(state):
        solved = True  # prevents further actions
        Game.print_actions('\nSolution:', solution)
        return

    actions = Game.get_possible_actions(state)

    for action in actions:
        if solved:
            return
        if DEBUG:
            Game.print_state(state)
        new_state = Game.take_action(action, state)
        solve(new_state, [*solution, action], depth + 1)  # recursive call

puzzles = Game.load_puzzles('puzzles.csv')

for puzzle in range(len(puzzles)):
    state = puzzles[puzzle + 1]
    print('\nPuzzle #' + str(puzzle + 1))
    Game.print_state(state)
    solved = False
    states_seen: Set[str] = set()
    solve(state, [])

# Solve a single puzzle instead of all.
# state = puzzles[1]
# print_puzzle(state)
# solve(state)
