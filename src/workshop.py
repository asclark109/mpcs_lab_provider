from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta


class Wrkshop():

    def __init__(self,shop_id:str, name:str) -> None:
        self.shop_id = shop_id
        self.name = name