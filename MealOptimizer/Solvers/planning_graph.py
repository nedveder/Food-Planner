from typing import Any, List, Tuple

from ..Problems.problem import Problem
from ..Solvers.solver import Solver


class PlanningGraphSolver(Solver):
    def __init__(self, max_levels: int = 10):
        self.max_levels = max_levels
        self.graph = None

    def solve(self, problem: 'Problem') -> Any:
        initial_state = problem.get_state()
        self.graph = self._build_planning_graph(problem, initial_state)
        return self._extract_solution(problem, self.graph)

    def _build_planning_graph(self, problem: 'Problem', initial_state: Any) -> List[Tuple[List[Any], List[Any]]]:
        graph = [(initial_state, problem.get_possible_actions(initial_state))]
        for _ in range(self.max_levels):
            prev_state, prev_actions = graph[-1]
            new_states = [problem.apply_action(prev_state, action) for action in prev_actions]
            new_actions = [problem.get_possible_actions(state) for state in new_states]
            graph.append((new_states, [action for sublist in new_actions for action in sublist]))
            if any(problem.is_goal_state(state) for state in new_states):
                break
        return graph

    def _extract_solution(self, problem: 'Problem', graph: List[Tuple[List[Any], List[Any]]]) -> Any:
        goal_level = next(i for i, (states, _) in enumerate(graph) if any(problem.is_goal_state(state) for state in states))
        goal_state = next(state for state in graph[goal_level][0] if problem.is_goal_state(state))

        solution = []
        for level in range(goal_level, 0, -1):
            prev_states, actions = graph[level - 1]
            action = next(action for action in actions if problem.apply_action(prev_states[0], action) == goal_state)
            solution.append(action)
            goal_state = prev_states[0]

        return list(reversed(solution))

    def get_iterations(self) -> int:
        return len(self.graph) if self.graph else 0
