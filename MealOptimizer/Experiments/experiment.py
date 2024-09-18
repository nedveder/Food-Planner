from typing import Dict
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
    def __init__(self, problem, solvers, start_date, piece_dataset_path, action_dataset_path, number_of_days=1, meals_per_day=3):
        self.solvers = solvers
        self.piece_dataset = _load_piece_dataset(piece_dataset_path)
        self.action_dataset = _load_action_dataset(action_dataset_path)
        self.current_state = self.create_initial_state(self.piece_dataset)
        pieces_with_dates = self.piece_dataset[["Product Name", "Date"]]
        self.problem = problem(self.action_dataset, start_date, pieces_with_dates,
                               number_of_days=number_of_days,
                               meals_per_day=meals_per_day)

    @staticmethod
    def create_initial_state(piece_dataset) -> State:
        available_pieces = []
        for index, row in piece_dataset.iterrows():
            piece = Piece(row["Product Name"], row["Quantity"], row["Unit"], row["Date"])
            available_pieces.append(piece)
        current_state = State(available_pieces)
        return current_state

    def run(self) -> Dict[str, State]:
        results = {}
        for solver in self.solvers:
            solver_final_state = solver.solve(self.problem, self.current_state)
            # Check that solver reached the goal state
            if not self.problem.is_goal_state(solver_final_state):
                print(f"{solver} did not reach the goal state")
                continue
            results[solver] = solver_final_state
            print(f"{solver} reached the goal state with score {self.problem.get_score(solver_final_state)}")
        return results
