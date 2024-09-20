import datetime
from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any
import re
import ast


from ..Problems.utils import Action, Piece


class Problem(ABC):
    def __init__(self, actions_dataset, start_date, pieces_with_dates, number_of_days=1, meals_per_day=3,
                 parameters_to_maximize: List[str] = None):
        self.start_date = start_date
        self.action_dataset = actions_dataset
        self.legal_actions = self.create_legal_actions(actions_dataset, pieces_with_dates)
        self.requested_amount = number_of_days * meals_per_day
        self.number_of_days = number_of_days
        self.meals_per_day = meals_per_day

    @staticmethod
    def create_legal_actions(action_dataset, pieces_with_dates) -> List[Action]:
        legal_actions = []
        for index, row in action_dataset.iterrows():
            pieces = []
            is_all_products_exist = True

            # Extract products from the 'Products' column using ast.literal_eval
            try:
                products = ast.literal_eval(row['Products'])
            except Exception as e:
                print(f"Error parsing products list at index {index}: {e}")
                continue

            # Process each product
            for product in products:
                try:
                    name = product.strip()
                    quantity = 1

                    if name not in pieces_with_dates["Product Name"].values:
                        # print(f"Product not found in dataset: {name}")
                        is_all_products_exist = False
                        break

                    expiration_date = pieces_with_dates[pieces_with_dates["Product Name"] == name]["Date"].values[0]
                    piece = Piece(name, quantity, expiration_date)
                    pieces.append(piece)
                except Exception as e:
                    print(f"Error processing product '{product}' at index {index}: {e}")
                    is_all_products_exist = False
                    break

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
        """State is all available products and used recipes, meaning available moves are all the recipes
        that can be made with the available products minus products used by recipes"""
        meals_cooked = len(state.selected_actions)
        current_date = self.start_date + datetime.timedelta(days=meals_cooked // self.meals_per_day)
        available_actions = []
        for action in self.legal_actions:
            if all(state.is_available_piece(piece, current_date) for piece in action.pieces):
                available_actions.append(action)
        return available_actions

    def get_score(self, state) -> float:
        """Calculate the score of the current state"""
        return sum(self.get_action_score(action) for action in state.selected_actions)

    def is_goal_state(self, state) -> bool:
        """Have we reached the requested amount of recipes"""
        return len(
            state.selected_actions) >= self.number_of_days * self.meals_per_day or not state.get_available_pieces