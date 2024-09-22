import copy
from typing import List, Dict

from ..Problems.utils import Action, Piece


class State:
    def __init__(self, available_pieces: List[Piece], selected_actions=None):
        if selected_actions is None:
            selected_actions = []
        self.selected_actions: List[Action] = selected_actions.copy()
        self.available_pieces: Dict[str, Piece] = {piece.item_id: piece for piece in copy.deepcopy(available_pieces)}

    def update_state(self, action) -> None:
        """Remove from available pieces all pieces used in the selected action"""
        self.selected_actions.append(action)
        for piece in action.pieces:
            if self.is_there_enough(piece):
                self.available_pieces[piece.item_id].quantity -= piece.quantity

    def is_there_enough(self, piece):
        return piece.item_id in self.available_pieces and self.available_pieces[piece.item_id].quantity >= piece.quantity

    def is_available_piece(self, piece, current_date) -> bool:
        """Check if the piece is available in the current state"""
        return self.is_there_enough(piece) and piece.expiration_date > current_date

    @property
    def get_selected_actions(self):
        return self.selected_actions

    @property
    def get_available_pieces(self):
        return list(self.available_pieces.values())

    def __repr__(self):
        selected_recipes = "\n".join([action.name for action in self.selected_actions])
        pieces_used = "\n".join(
            [f"{piece.item_id} {piece.quantity}" for action in self.selected_actions for piece in action.pieces])
        return f"Selected recipes: \n{selected_recipes} \nProducts used: \n{pieces_used}"

    def __copy__(self):
        return State(list(self.available_pieces.values()), self.selected_actions)
