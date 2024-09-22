import copy
import datetime
from typing import List


class Piece:
    def __init__(self, item_id, quantity, expiration_date=None):
        self.item_id = item_id
        self.quantity = int(quantity)
        # Format date time
        if expiration_date:
            for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
                try:
                    self.expiration_date = datetime.datetime.strptime(expiration_date, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                # If none of the formats match, raise an error
                raise ValueError(f"Invalid date format: {expiration_date}")

    def __hash__(self):
        return hash((self.item_id, self.quantity, self.expiration_date))


class Action:
    def __init__(self, action_id, name, pieces: List[Piece]):
        self.action_id = action_id
        self.name = name
        self.pieces = pieces

    def __hash__(self):
        return hash((self.action_id, self.name, tuple(self.pieces)))
