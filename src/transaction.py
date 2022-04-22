class Trnsctn():

    def __init__(self, trns_id:str, resv_id:str, desc:str, date: str, amnt: float, billtyp: str) -> None:
        self.trns_id = trns_id
        self.resv_id = resv_id
        self.desc = desc
        self.date = date
        self.amnt = amnt
        self.billtyp = billtyp
