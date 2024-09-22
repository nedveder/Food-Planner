import copy
import datetime
from typing import List


class Piece:
    def __init__(self, item_id, quantity, expiration_date=None):
        self.item_id = item_id
        self.quantity = int(quantity)
        # Format date time
        year, month, day = expiration_date.split("-")
        self.expiration_date = datetime.date(int(year), int(month), int(day)) if expiration_date else None

    def __hash__(self):
        return hash((self.item_id, self.quantity, self.expiration_date))


class Action:
    def __init__(self, action_id, name, pieces: List[Piece]):
        self.action_id = action_id
        self.name = name
        self.pieces = pieces

    def __hash__(self):
        return hash((self.action_id, self.name, tuple(self.pieces)))
