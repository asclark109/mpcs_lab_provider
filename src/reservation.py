from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta

from equipment import Eqpment
from transaction import Trnsctn
from workshop import Wrkshop

class Resrvtn():

    def __init__(self, resv_id:str, custID:str, date_bk:str, date_rs:str, d_o_w:str, hr_strt:int, mm_strt:int, canceld:bool = False) -> None:
        self.resv_id = resv_id
        self.custID = custID
        self.date_bk = date_bk
        self.date_rs = date_rs
        self.d_o_w = d_o_w
        self.hr_strt = hr_strt
        self.mm_strt = mm_strt
        self.eqmnt = None
        self.wrkshop = None
        self.canceld = canceld
        self.trncns = []

    def add_eqp(self, eqpmnt: Eqpment):
        self.eqmnt = eqpmnt

    def add_wrk(self, wrkshop: Wrkshop):
        self.wrkshop = wrkshop

    def add_trn(self, trnsctn: Trnsctn):
        self.trncns.append(trnsctn)

    def calcDwn(self, subtotl:float):
        if self.eqmnt is not None:
            return 0.5*subtotl
        else:
            return 0
  
    def calcCst(self) -> float:
        if self.wrkshop is not None:
            return 99*0.5
        
        if self.eqmnt is not None:
            if self.eqmnt.eq_type == "Micrvac":
                return 1000*0.5
            if self.eqmnt.eq_type == "Irradtr":
                return 2220*0.5
            if self.eqmnt.eq_type == "PlymExt":
                return 600*0.5
            if self.eqmnt.eq_type == "HiVelCr":
                return 10000
            if self.eqmnt.eq_type == "LiHrvst":
                return 8800*0.5
            
    def calcDis(self, date_bk:str, date_rs:str, totbill:float) -> float:
        book_dt = datetime.strptime(date_bk,'%m/%d/%Y').date()
        resv_dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
        delta = resv_dt - book_dt
        if delta.days >= 14:
            return totbill*0.25
        else:
            return 0

    def calcRef(self, date_rs:str, dwnpay:float) -> float:
        today = date.today()
        resv_dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
        delta = resv_dt - today
        if delta.days >= 7:
            return dwnpay*0.75
        elif delta.days >= 2:
            return dwnpay*0.75
        else:
            return 0

    def hasRfnd(self) -> bool:
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == "refund (cancellation)":
                return True
        return False

    def getRef(self) -> Trnsctn:
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == "refund (cancellation)":
                return trnsctn
        return None

    def hasDwnP(self) -> bool:
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == r"50% down payment":
                return True
        return False

    def getDwnP(self) -> Trnsctn:
        trnsctn: Trnsctn
        for trnsctn in self.trncns:
            if trnsctn.desc == r"50% down payment":
                return trnsctn
        return trnsctn

    def __repr__(self) -> str:
        name = self.wrkshop.name if self.wrkshop is not None else ""
        name = self.eqmnt.eq_name if self.eqmnt is not None else name
        time = "{}:{}".format(self.hr_strt,str(self.mm_strt).zfill(2))
        return "<reservation: id= {}, dt_rs= {}, time_st= {}, type= {}>".format(self.resv_id,self.date_rs,time,name)
