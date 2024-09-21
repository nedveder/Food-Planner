import random
from typing import Dict, Tuple, List
from ..Problems.problem import Problem
from ..Problems.state import State
from ..Problems.utils import Action, Piece
from .solver import Solver


class RLSolver(Solver):
    def __init__(self, learning_rate=0.5, discount_factor=0.95, epsilon=0.1, episodes=1000):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.episodes = episodes
        self.q_table: Dict[Tuple[Tuple[str], str], float] = {}

    def solve(self, problem: Problem, initial_state: State) -> State:
        """
        Solve the given problem using Q-learning and return the best solution found.
        """
        best_state = None
        best_score = float('-inf')

        for _ in range(self.episodes):
            state = initial_state.__copy__()

            while not problem.is_goal_state(state):
                available_actions = problem.get_available_actions(state)
                if not available_actions:
                    break

                action = self.choose_action(problem, state, available_actions)
                next_state = state.__copy__()
                next_state.update_state(action)

                reward = problem.get_action_score(action,state)
                self.update_q_value(state, action, reward, next_state, problem)

                state = next_state

            score = problem.get_score(state)
            if score > best_score:
                best_score = score
                best_state = state

        return best_state

    def choose_action(self, problem: Problem, state: State, available_actions: List[Action]) -> Action:
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        else:
            return max(available_actions, key=lambda a: self.get_q_value(state, a))

    def update_q_value(self, state: State, action: Action, reward: float, next_state: State, problem: Problem):
        current_q = self.get_q_value(state, action)
        max_next_q = max(
            self.get_q_value(next_state, a) for a in problem.get_available_actions(next_state)) if problem.get_available_actions(
            next_state) else 0
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[self.state_action_to_key(state, action)] = new_q

    def get_q_value(self, state: State, action: Action) -> float:
        return self.q_table.get(self.state_action_to_key(state, action), 0.0)

    @staticmethod
    def state_action_to_key(state: State, action: Action) -> Tuple[Tuple[str], str]:
        state_key = tuple(sorted(p.item_id for p in state.get_available_pieces))
        return (state_key, action.action_id)