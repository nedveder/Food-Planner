from typing import List
from ..Problems.problem import Problem
from ..Problems.state import State
from ..Problems.utils import Action
from .solver import Solver


class GreedySolver(Solver):
    def solve(self, problem: Problem, state: State) -> State:
        """
        Solve the given problem using a greedy approach and return the solution.
        """
        while not problem.is_goal_state(state):
            available_actions = problem.get_available_actions(state)
            if not available_actions:
                break  # No more actions available, terminate

            # Find the action with the highest score
            best_action = max(available_actions, key=lambda act: problem.get_action_score(act, state))

            # Update the state with the best action
            state.update_state(best_action)

        return state
