import time
from typing import Dict, Tuple
import pandas as pd

from ..Problems.state import State
from ..Problems.utils import Piece


def _load_piece_dataset(piece_dataset_path) -> pd.DataFrame:
    try:
        return pd.read_csv(piece_dataset_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Product dataset not found at {piece_dataset_path}")


def _load_action_dataset(action_dataset_path) -> pd.DataFrame:
    try:
        return pd.read_csv(action_dataset_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Product dataset not found at {action_dataset_path}")


class Experiment:
    def __init__(self, problem, solvers, start_date, piece_dataset, action_dataset, number_of_days=1,
                 meals_per_day=3, parameters=None):
        self.solvers = solvers
        self.piece_dataset = piece_dataset
        self.action_dataset = action_dataset
        self.current_state = None
        self.pieces_with_dates = self.piece_dataset[["Product Name", "Date"]]
        self.start_date = start_date
        self.number_of_days = number_of_days
        self.meals_per_day = meals_per_day
        self.parameters = parameters
        self.problem = problem

    @staticmethod
    def create_initial_state(piece_dataset) -> State:
        available_pieces = []
        for index, row in piece_dataset.iterrows():
            piece = Piece(row["Product Name"], row["Quantity"], row["Date"])
            available_pieces.append(piece)
        current_state = State(available_pieces)
        return current_state

    def run(self) -> Dict[str, Tuple[State, float]]:
        results = {}
        for solver in self.solvers:
            problem = self.problem(self.action_dataset, self.start_date, self.pieces_with_dates,
                                   number_of_days=self.number_of_days,
                                   meals_per_day=self.meals_per_day,
                                   parameters_to_maximize=self.parameters)
            self.current_state = self.create_initial_state(self.piece_dataset)
            start_time = time.time()
            solver_final_state = solver.solve(problem, self.current_state)
            end_time = time.time()
            solver_time = end_time - start_time

            if problem.is_goal_state(solver_final_state):
                results[solver] = (solver_final_state, solver_time, problem.get_score(solver_final_state))
                print(f"{solver} reached the goal state with score {problem.get_score(solver_final_state)}")
            else:
                results[solver] = (None, solver_time, 0)
                print(f"{solver} did not reach the goal state")
        return results
