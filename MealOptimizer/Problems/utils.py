from typing import List


class Piece:
    def __init__(self, item_id, quantity, unit, expiration_date=None):
        self.item_id = item_id
        self.quantity = quantity
        self.unit = unit
        self.expiration_date = expiration_date


class Action:
    def __init__(self, action_id, pieces: List[Piece]):
        self.action_id = action_id
        self.pieces = pieces
