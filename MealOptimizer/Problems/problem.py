from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any

from ..Problems.utils import Action, Piece


class Problem(ABC):
    def __init__(self, actions_dataset, start_date, pieces_with_dates, requested_amount=2):
        """Legal actions is all available recipies that can be made in this current dataset"""
        self.start_date = start_date
        self.action_dataset = actions_dataset
        self.legal_actions = self.create_legal_actions(actions_dataset, pieces_with_dates)
        self.requested_amount = requested_amount

    @staticmethod
    def create_legal_actions(action_dataset, pieces_with_dates) -> List[Action]:
        legal_actions = []
        for index, row in action_dataset.iterrows():
            pieces = []
            is_all_products_exist = True
            for product in row["Products"].split(","):
                name, quantity = product.split("(")
                quantity, unit = quantity[:-1].split(" ")
                if name not in pieces_with_dates["Product Name"].values:
                    print("Product not found in dataset")
                    is_all_products_exist = False
                    break
                expiration_date = pieces_with_dates[pieces_with_dates["Product Name"] == name]["Date"].values[0]
                piece = Piece(name, quantity, unit, expiration_date)
                pieces.append(piece)
            if not is_all_products_exist:
                continue
            action = Action(row["Recipe ID"], row["Recipe Name"], pieces)
            legal_actions.append(action)
        return legal_actions

    @abstractmethod
    def get_action_score(self, action) -> float:
        """Action is selected recipe"""
        pass

    def get_available_actions(self, state) -> List[Action]:
        """State is all available products and used recipies, meaning available moves are all the recipies
        that can be made with the available products minus products used by recipies"""
        available_actions = []
        for action in self.legal_actions:
            if all(state.is_available_piece(piece) for piece in action.pieces):
                available_actions.append(action)
        return available_actions

    def get_score(self, state) -> float:
        """Calculate the score of the current state"""
        return sum(self.get_action_score(action) for action in state.selected_actions)

    def is_goal_state(self, state) -> bool:
        """Have we reached the requested amount of recipies"""
        return len(state.selected_actions) == self.requested_amount
