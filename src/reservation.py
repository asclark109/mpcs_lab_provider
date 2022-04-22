"""module holding Reservation class. This is the focal domain entity of program"""

# external
from __future__ import annotations
from datetime import datetime, date, timedelta

# local
from bookable_item import BookableItem
from transaction import Transaction

class Reservation():

    def __init__(self, resv_id:str, custID:str, date_bk:datetime, date_rs:datetime, bookable_item: BookableItem, duration: float, canceld:bool = False) -> None:
        self.resv_id = resv_id
        self.custID = custID
        self.canceld = canceld
        self.trncns = []
        self.bookable_item = bookable_item
        self.start_datetime = date_rs
        self.duration = duration
        self.time_of_creation_datetime = date_bk
        self.end_datetime = self.start_datetime + timedelta(hours = self.duration)
        self.inadvance_datetime = self.start_datetime - self.time_of_creation_datetime

    # not used
    def set_bookable_item(self, bookable_item: BookableItem):
        self.bookable_item = bookable_item    

    def add_transaction(self, trnsctn: Transaction):
        self.trncns.append(trnsctn)

    def calc_downpayment(self):
        # if it has equipment it will be 50% subtotal; else, it is 
        # a workshop and refund will be 0.
        total_cost = self.calc_tot_cost()
        discount = self.calc_discount(total_cost)
        subtotal = total_cost - discount
        downpayment_frac = self.bookable_item.downpayment_fraction()
        return downpayment_frac*subtotal
  
    def calc_tot_cost(self) -> float:
        hours = self.duration # in hours
        return self.bookable_item.cost_per_hour()*hours
            
    def cancel(self)->None:
        self.canceld = True

    def calc_discount(self, totbill:float) -> float:
        if self.inadvance_datetime.days >= 14:
            return totbill*0.25
        else:
            return 0

    def calc_refund(self) -> float:
        # determine how many days from now till reservation
        today = date.today()
        reservation_date = self.start_datetime.date() # datetime.strptime(date_rs,'%m/%d/%Y').date()
        delta = reservation_date - today

        # calc downpayment
        downpayment = self.calc_downpayment()
        if delta.days >= 7:
            return downpayment*0.75
        elif delta.days >= 2:
            return downpayment*0.50
        else:
            return 0

    def has_refund(self) -> bool:
        trnsctn: Transaction
        for trnsctn in self.trncns:
            if trnsctn.desc == "refund (cancellation)":
                return True
        return False

    def get_refund(self) -> Transaction:
        trnsctn: Transaction
        for trnsctn in self.trncns:
            if trnsctn.desc == "refund (cancellation)":
                return trnsctn
        return None

    def has_downpayment(self) -> bool:
        trnsctn: Transaction
        for trnsctn in self.trncns:
            if trnsctn.desc == r"50% down payment":
                return True
        return False

    def get_downpayment(self) -> Transaction:
        trnsctn: Transaction
        for trnsctn in self.trncns:
            if trnsctn.desc == r"50% down payment":
                return trnsctn
        return trnsctn

    def overlaps_with_window(self,datetime_st:datetime,datetime_end:datetime)->bool:
        """returns true if this reservations start and end time
        are such that it overlaps with the other_reservations'
        start and end time."""
        bool1 = self.start_datetime < datetime_end
        bool2 = datetime_st < self.end_datetime
        return bool1 and bool2

    def __repr__(self) -> str:
        booked_item_name = self.bookable_item.get_name()
        return "<reservation: id= {}, date= {}, duration(hrs)= {}, item= {}>".format(self.resv_id,self.start_datetime,self.duration,booked_item_name)
