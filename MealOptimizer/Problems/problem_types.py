import datetime
from typing import List

from .state import State
from .utils import Action
from ..Problems import Problem

MAX_PARAMETERS = {"Shelf Time", "Taste Rating"}
MIN_PARAMETERS = {"Number of Steps", "Preparation Time (min)", "Number of Products"}


class MinimizeWasteProblem(Problem):
    def get_action_score(self, action, state: State = None) -> float:
        """
        Score is the sum of the inverse difference between the expiration date of the products and the current date,
        meaning the closer the expiration date the higher the score.
        The goal is to minimize waste, so we want to use products that are closer to expiration date.
        """
        if state is None:
            raise RuntimeError("State is required for this problem.")
        expired_count = 0
        meals_cooked = len(state.selected_actions)
        tomorrow_date = self.start_date + datetime.timedelta(days=1 + (meals_cooked // self.meals_per_day))
        for piece in state.get_available_pieces:
            if piece.expiration_date < tomorrow_date and piece.quantity > 0 and piece not in action.pieces:
                expired_count += 1

        score = 0
        for piece in action.pieces:
            score += 1 / ((piece.expiration_date - self.start_date).days + 1)
        return score+1/(expired_count+1)


class CountExpiredItemsProblem(Problem):
    def get_action_score(self, action: Action, state: State = None) -> float:
        """
        Score is the negative count of items that would expire if not used in this action.
        The goal is to minimize the number of expired items.
        """
        if state is None:
            raise RuntimeError("State is required for this problem.")
        expired_count = 0
        meals_cooked = len(state.selected_actions)
        tomorrow_date = self.start_date + datetime.timedelta(days=1 + (meals_cooked // self.meals_per_day))
        for piece in state.get_available_pieces:
            if piece.expiration_date < tomorrow_date and piece.quantity > 0 and piece not in action.pieces:
                expired_count += 1

        return 1 / (expired_count + 1)


class ParametersProblem(Problem):
    def __init__(self, actions_dataset, start_date, pieces_with_dates, number_of_days=2, meals_per_day=3,
                 parameters_to_maximize: List[str] = None):
        super().__init__(actions_dataset, start_date, pieces_with_dates, number_of_days, meals_per_day)
        self.parameters_to_maximize = parameters_to_maximize or []

        # Validate that all specified parameters exist in the dataset
        for param in self.parameters_to_maximize:
            if param not in self.action_dataset.columns:
                raise ValueError(f"Parameter '{param}' not found in the action dataset.")

        # Normalize the parameters
        self.normalized_parameters = self._normalize_parameters()

    def _normalize_parameters(self):
        normalized = {}
        for param in self.parameters_to_maximize:
            min_val = self.action_dataset[param].min()
            max_val = self.action_dataset[param].max()
            if min_val == max_val:
                normalized[param] = self.action_dataset[param].apply(lambda x: 1)
            else:
                normalized[param] = (self.action_dataset[param] - min_val) / (max_val - min_val)
        return normalized

    def get_score_by_minimize(self, action: Action, param) -> float:
        """
        Score is the sum of the normalized values of the specified parameters for the given action.
        The goal is to minimize these parameters.
        """
        score = 0
        for piece in action.pieces:
            score += 1 / ((piece.expiration_date - self.start_date).days + 1)

        normalized_value = self.normalized_parameters[param][self.action_dataset['Recipe ID'] == action.action_id].values[0]
        score += normalized_value

    def get_action_score(self, action: Action, state: State = None) -> float:
        """
        Score is the sum of the normalized values of the specified parameters for the given action.
        The goal is to maximize these parameters.
        """
        score = 0
        for piece in action.pieces:
            score += 1 / ((piece.expiration_date - self.start_date).days + 1)

        for param in self.parameters_to_maximize:
            if param in MAX_PARAMETERS:
                normalized_value = self.normalized_parameters[param][self.action_dataset['Recipe ID'] == action.action_id].values[0]
                score += normalized_value
            elif param in MIN_PARAMETERS:
                normalized_value = self.normalized_parameters[param][self.action_dataset['Recipe ID'] == action.action_id].values[0]
                score -= normalized_value
        return score
