import random
import math
from typing import List, Tuple
from ..Problems.problem import Problem
from ..Problems.state import State
from ..Problems.utils import Action
from .solver import Solver


class SimulatedAnnealingSolver(Solver):
    def __init__(self, initial_temperature: float = 1000.0, cooling_rate: float = 0.995, iterations: int = 1000):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.iterations = iterations

    def solve(self, problem: Problem, initial_state: State) -> State:
        current_state = initial_state
        best_state = current_state
        temperature = self.initial_temperature

        for _ in range(self.iterations):
            if problem.is_goal_state(current_state):
                break

            neighbor_state = self.get_neighbor_state(problem, current_state)
            current_score = problem.get_score(current_state)
            neighbor_score = problem.get_score(neighbor_state)

            if self.accept_probability(current_score, neighbor_score, temperature) > random.random():
                current_state = neighbor_state

            if problem.get_score(current_state) > problem.get_score(best_state):
                best_state = current_state

            temperature *= self.cooling_rate

        return best_state

    def get_neighbor_state(self, problem: Problem, current_state: State) -> State:
        new_state = State(current_state.get_available_pieces.copy())
        new_state.selected_actions = current_state.get_selected_actions.copy()

        if len(new_state.selected_actions) > 0 and random.random() < 0.5:
            # Remove a random action
            removed_action = new_state.selected_actions.pop(random.randrange(len(new_state.selected_actions)))
            for piece in removed_action.pieces:
                for available_piece in new_state.available_pieces:
                    if available_piece.item_id == piece.item_id and available_piece.unit == piece.unit:
                        available_piece.quantity += piece.quantity
                        break

        # Add a new random action
        available_actions = problem.get_available_actions(new_state)
        if available_actions:
            new_action = random.choice(available_actions)
            new_state.update_state(new_action)

        return new_state

    @staticmethod
    def accept_probability(current_score: float, new_score: float, temperature: float) -> float:
        if new_score > current_score:
            return 1.0
        return math.exp((new_score - current_score) / temperature)
