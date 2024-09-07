import datetime
from typing import List


class Piece:
    def __init__(self, item_id, quantity, unit, expiration_date=None):
        self.item_id = item_id
        self.quantity = int(quantity)
        self.unit = unit
        # Format date time
        year, month, day = expiration_date.split("-")
        self.expiration_date = datetime.date(int(year), int(month), int(day)) if expiration_date else None


class Action:
    def __init__(self, action_id, name, pieces: List[Piece]):
        self.action_id = action_id
        self.name = name
        self.pieces = pieces
