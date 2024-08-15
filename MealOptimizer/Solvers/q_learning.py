import random
from typing import Any, List, Tuple, Dict

from ..Problems.problem import Problem
from ..Solvers.solver import Solver


class RLSolver(Solver):
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, epsilon: float = 0.1, episodes: int = 1000):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.episodes = episodes
        self.q_table: Dict[Tuple[Any, Any], float] = {}

    def solve(self, problem: 'Problem') -> Any:
        for _ in range(self.episodes):
            state = problem.get_state()
            while not problem.is_goal_state(state):
                action = self._choose_action(problem, state)
                next_state = problem.apply_action(state, action)
                reward = problem.evaluate_solution()['total_score']
                self._update_q_value(state, action, reward, next_state)
                state = next_state

        return self._get_best_solution(problem)

    def _choose_action(self, problem: 'Problem', state: Any) -> Any:
        if random.random() < self.epsilon:
            return random.choice(problem.get_possible_actions(state))
        else:
            return max(problem.get_possible_actions(state), key=lambda a: self.q_table.get((state, a), 0))

    def _update_q_value(self, state: Any, action: Any, reward: float, next_state: Any):
        current_q = self.q_table.get((state, action), 0)
        next_max_q = max(self.q_table.get((next_state, a), 0) for a in Problem.get_possible_actions(next_state))
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[(state, action)] = new_q

    def _get_best_solution(self, problem: 'Problem') -> Any:
        state = problem.get_state()
        solution = []
        while not problem.is_goal_state(state):
            action = max(problem.get_possible_actions(state), key=lambda a: self.q_table.get((state, a), 0))
            solution.append(action)
            state = problem.apply_action(state, action)
        return solution

    def get_iterations(self) -> int:
        return self.episodes
