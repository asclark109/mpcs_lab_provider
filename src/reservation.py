from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta




from bookable_item import BookableItem
# from equipment import Equipment
from transaction import Trnsctn
# from workshop import Wrkshop

class Reservation():

    def __init__(self, resv_id:str, custID:str, date_bk:datetime, date_rs:datetime, bookable_item: BookableItem, duration: float, canceld:bool = False) -> None:
        # d_o_w:str, hr_strt:int, mm_strt:int, 
        self.resv_id = resv_id
        self.custID = custID
        # self.date_bk = date_bk
        # self.date_rs = date_rs
        # self.d_o_w = d_o_w
        # self.hr_strt = hr_strt
        # self.mm_strt = mm_strt
        # self.eqmnt = None
        # self.wrkshop = None
        self.canceld = canceld
        self.trncns = []
        self.bookable_item = bookable_item
        

        self.start_datetime = date_rs
        self.duration = duration
        self.time_of_creation_datetime = date_bk
        self.end_datetime = self.start_datetime + timedelta(hours = self.duration)
        self.inadvance_datetime = self.start_datetime - self.time_of_creation_datetime


    def set_bookable_item(self, bookable_item: BookableItem):
        self.bookable_item = bookable_item    

    # def add_equipemnt(self, eqpmnt: Equipment):
    #     self.eqmnt = eqpmnt

    # def add_workshop(self, wrkshop: Wrkshop):
    #     self.wrkshop = wrkshop

    def add_transaction(self, trnsctn: Trnsctn):
        self.trncns.append(trnsctn)

    def calc_downpayment(self):
        # if it has equipment it will be 50% subtotal; else, it is 
        # a workshop and refund will be 0.
        total_cost = self.calc_tot_cost()
        discount = self.calc_discount(total_cost)
        subtotal = total_cost - discount
        downpayment_frac = self.bookable_item.downpayment_fraction()
        return downpayment_frac*subtotal
        # if self.eqmnt is not None:
        #     return 0.5*subtotl
        # else:
        #     return 0
  
    def calc_tot_cost(self) -> float:
        hours = self.duration # in hours
        return self.bookable_item.cost_per_hour()*hours
        # if self.wrkshop is not None:
        #     return 99*0.5
        
        # if self.eqmnt is not None:
        #     if self.eqmnt.eq_type == "Micrvac":
        #         return 1000*0.5
        #     if self.eqmnt.eq_type == "Irradtr":
        #         return 2220*0.5
        #     if self.eqmnt.eq_type == "PlymExt":
        #         return 600*0.5
        #     if self.eqmnt.eq_type == "HiVelCr":
        #         return 10000
        #     if self.eqmnt.eq_type == "LiHrvst":
        #         return 8800*0.5
            
    def cancel(self)->None:
        self.canceld = True

    def calc_discount(self, totbill:float) -> float:
        # book_dt = datetime.strptime(date_bk,'%m/%d/%Y').date()
        # resv_dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
        if self.inadvance_datetime.days >= 14:
            return totbill*0.25
        else:
            return 0
        # delta = resv_dt - book_dt
        # if delta.days >= 14:
        #     return totbill*0.25
        # else:
        #     return 0

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
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == "refund (cancellation)":
                return True
        return False

    def get_refund(self) -> Trnsctn:
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == "refund (cancellation)":
                return trnsctn
        return None

    def has_downpayment(self) -> bool:
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == r"50% down payment":
                return True
        return False

    def get_downpayment(self) -> Trnsctn:
        trnsctn: Trnsctn
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
        # name = self.wrkshop.name if self.wrkshop is not None else ""
        # name = self.eqmnt.eq_name if self.eqmnt is not None else name
        # time = "{}:{}".format(self.start_datetime)
        return "<reservation: id= {}, date= {}, duration(hrs)= {}, item= {}>".format(self.resv_id,self.start_datetime,self.duration,booked_item_name)
