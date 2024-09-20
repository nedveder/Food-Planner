from typing import List

from ..Problems.utils import Action, Piece


class State:
    def __init__(self, available_pieces: List[Piece], selected_actions=None):
        if selected_actions is None:
            selected_actions = []
        self.selected_actions: List[Action] = selected_actions
        self.available_pieces: List[Piece] = available_pieces

    def update_state(self, action) -> None:
        """Remove from available pieces all pieces used in the selected action"""
        self.selected_actions.append(action)
        for piece in action.pieces:
            for available_piece in self.available_pieces:
                if self.is_there_enough(available_piece, piece):
                    available_piece.quantity -= piece.quantity

    @staticmethod
    def is_there_enough(available_piece, piece):
        return available_piece.item_id == piece.item_id and \
            available_piece.quantity >= piece.quantity

    def is_available_piece(self, piece, current_date) -> bool:
        """Check if the piece is available in the current state"""
        for available_piece in self.available_pieces:
            if piece.expiration_date > current_date and self.is_there_enough(available_piece, piece):
                return True
        return False

    @property
    def get_selected_actions(self):
        return self.selected_actions

    @property
    def get_available_pieces(self):
        return self.available_pieces

    def __repr__(self):
        selected_recipes = "\n".join([action.name for action in self.selected_actions])
        pieces_used = "\n".join(
            [f"{piece.item_id} {piece.quantity}" for action in self.selected_actions for piece in action.pieces])
        return f"Selected recipes: \n{selected_recipes} \nProducts used: \n{pieces_used}"

    def __copy__(self):
        return State(self.available_pieces.copy(), self.selected_actions.copy())
