import math
import random
from typing import Any, List, Tuple

from ..Problems.problem import Problem
from ..Solvers.solver import Solver


class RandomizedSolver(Solver):
    def __init__(self, initial_temperature: float = 100, cooling_rate: float = 0.995, iterations: int = 1000):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.iterations = iterations

    def solve(self, problem: 'Problem') -> Any:
        current_state = problem.get_state()
        current_score = problem.evaluate_solution()['total_score']
        best_state = current_state
        best_score = current_score
        temperature = self.initial_temperature

        for _ in range(self.iterations):
            neighbor = self._get_neighbor(problem, current_state)
            neighbor_score = problem.evaluate_solution()['total_score']

            if self._accept_move(current_score, neighbor_score, temperature):
                current_state = neighbor
                current_score = neighbor_score

            if current_score > best_score:
                best_state = current_state
                best_score = current_score

            temperature *= self.cooling_rate

        return best_state

    def _get_neighbor(self, problem: 'Problem', state: Any) -> Any:
        actions = problem.get_possible_actions(state)
        return problem.apply_action(state, random.choice(actions))

    def _accept_move(self, current_score: float, neighbor_score: float, temperature: float) -> bool:
        if neighbor_score > current_score:
            return True
        return random.random() < math.exp((neighbor_score - current_score) / temperature)

    def get_iterations(self) -> int:
        return self.iterations
