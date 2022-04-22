from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta

from bookable_item import BookableItem


class Workshop(BookableItem):

    DOWN_PAYMENT_FRAC = 0
    COST_PER_HOUR = 99

    def __init__(self,shop_id:str, name:str) -> None:
        self.shop_id = shop_id
        self.name = name

    def get_id(self) -> str:
        return self.shop_id

    def get_name(self) -> str:
        return self.name

    def cost_per_hour(self) -> float:
        return self.COST_PER_HOUR

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC
    