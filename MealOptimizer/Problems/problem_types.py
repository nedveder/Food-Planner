from datetime import date

from ..Problems import Problem


class MinimizeWasteProblem(Problem):
    def get_action_score(self, action) -> float:
        """
        Score is the sum of the inverse difference between the expiration date of the products and the current date,
        meaning the closer the expiration date the higher the score.
        The goal is to minimize waste, so we want to use products that are closer to expiration date.
        """
        score = 0
        for piece in action.pieces:
            score += 1 / ((piece.expiration_date - self.start_date).days + 1)
        return score


class MaximizeByParametersProblem(Problem):
    def __init__(self, legal_actions, requested_amount, parameters):
        super().__init__(legal_actions, requested_amount)
        self.parameters = parameters

    def get_action_score(self, action) -> float:
        # TODO
        return 0
