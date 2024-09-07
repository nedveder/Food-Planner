from typing import List

from ..Problems.utils import Action, Piece


class State:
    def __init__(self, available_pieces: List[Piece]):
        self.selected_actions: List[Action] = []
        self.available_pieces: List[Piece] = available_pieces

    def update_state(self, action) -> None:
        """Remove from available pieces all pieces used in the selected action"""
        pass

    def is_available_piece(self, piece) -> bool:
        """Check if the piece is available in the current state"""
        for available_piece in self.available_pieces:
            if (available_piece.item_id == piece.item_id and
                    available_piece.unit == piece.unit and
                    available_piece.quantity >= piece.quantity):
                return True
        return False

    @property
    def get_selected_actions(self):
        return self.selected_actions

    @property
    def get_available_pieces(self):
        return self.available_pieces
