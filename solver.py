# global-statement: Using the global statement
# pylint: disable=W0603

from typing import List, Set
from lunar_lockout import Action, LunarLockout as Game, State

DEBUG = False

def visited(state: State) -> bool:
    global visited_states
    key = Game.state_string(state)
    seen = key in visited_states
    if not seen:
        visited_states.add(key)
    return seen

def solve(state: State, solution: List[Action]) -> None:
    global solved

    if visited(state):
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
        solve(new_state, [*solution, action])  # recursive call

puzzles = Game.load_puzzles('puzzles.csv')

for i in range(1, len(puzzles) + 1):
    state = puzzles[i]
    print('\nPuzzle #' + str(i))
    Game.print_state(state)
    solved = False
    visited_states: Set[str] = set()
    solve(state, [])

# Solve a single puzzle instead of all.
# state = puzzles[1]
# print_puzzle(state)
# solve(state, [])
