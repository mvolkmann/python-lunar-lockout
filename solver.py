# global-statement: Using the global statement
# pylint: disable=W0603

import sys
from typing import List, Set
#from lunar_lockout import Action, LunarLockout as Game, State
from tilt import Action, Tilt as Game, State

DEBUG = False

solution = None

def optimize(state: State, actions: List[Action]) -> List[Action]:
    """Look for unnecessary actions and remove them."""
    for i in range(len(actions) - 1):
        # Create a copy of actions with the i'th action removed.
        actions_copy = actions.copy()
        del actions_copy[i]

        try:
            # Replay these actions.
            state_copy = state.copy()
            for action in actions_copy:
                state_copy = Game.take_action(state_copy, action)

            # If the puzzle can be solved without that action,
            # use these actions.
            if Game.is_solved(state_copy):
                return optimize(state, actions_copy)
        except ValueError:
            pass  # ingore since we are just trying alternate solutions

    return actions

def report() -> None:
    global solution
    if solution:
        solution = optimize(state, solution)
        Game.print_actions('Solution:', solution)
    else:
        print('No solution found.')

def solve(state: State, actions_taken: List[Action]) -> None:
    """Solve a puzzle with given starting State."""
    global solution

    if visited(state):
        return

    if Game.is_solved(state):
        solution = actions_taken
        return

    print('solver.py solve: state =', state)
    new_actions = Game.get_possible_actions(state)
    print('solver.py solve: new_actions =', new_actions)
    for new_action in new_actions:
        if solution:
            return
        if DEBUG:
            Game.print_state(state)
        new_state = Game.take_action(state, new_action)
        print('solver.py solve: new_state =', new_state)
        solve(new_state, [*actions_taken, new_action])  # recursive call

def visited(state: State) -> bool:
    """Determine if a given State has already been visited."""
    global visited_states
    key = Game.state_string(state)
    seen = key in visited_states
    if not seen:
        visited_states.add(key)
    return seen

#puzzles = Game.load_puzzles('lunar_lockout.csv')
puzzles = Game.load_puzzles('tilt.csv')

visited_states: Set[str] = set()

# for i in range(1, len(puzzles) + 1):
#     state = puzzles[i]
#     print('\nPuzzle #' + str(i))
#     Game.print_state(state)
#     solution = None
#     visited_states.clear()
#     solve(state, [])
#     report()

# Solve a single puzzle instead of all.
state = puzzles[1]
Game.print_state(state)
solve(state, [])
report()
