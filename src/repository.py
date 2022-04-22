from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta

from reservation import Resrvtn
from equipment import Eqpment
from transaction import Trnsctn
from workshop import Wrkshop

######### REPO #########

class ObjRepo():

    DATA_PATH = "db/"
    TRN_FILE = DATA_PATH + "trnsctn.txt"
    RSV_FILE = DATA_PATH + "rsrvtns.txt"
    WKS_FILE = DATA_PATH + "wrkshps.txt"
    EQM_FILE = DATA_PATH + "eqmnt.txt"

    def __init__(self) -> None:
        pass

    def getRsvn(self, rsvn_id:str) -> Resrvtn:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            c_rv_id = line[0]
            if rsvn_id == c_rv_id:
                cust_id = line[1]
                d_o_w = line[2]
                date_bk = line[3]
                date_rs = line[4]
                hr_strt = int(line[5])
                mm_strt = int(line[6])
                eq_id = line[7]
                wksp_id = line[8]
                canceld = bool(int(line[9]))
            
                rsvn = Resrvtn(rsvn_id,cust_id,date_bk,date_rs,hr_strt,mm_strt,canceld)

                if wksp_id != "":
                    wkshop = self.getWkp(wksp_id)
                    rsvn.add_wrk(wkshop)
                elif eq_id != "":
                    eqpmnt = self.getEqmt(eq_id)
                    rsvn.add_eqp(eqpmnt)

                return rsvn
        
        return None

    def getEqmt(self, eq_id:str) -> Eqpment:
        with open(self.EQM_FILE) as f:
            lines = f.readlines()

        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            c_eq_id = line[0]
            if eq_id == c_eq_id:
                eq_name = line[1]
                eq_type = line[2]
            
                eqmnt = Eqpment(eq_id,eq_type,eq_name)
                return eqmnt
        
        return None        

    def getEqTp(self, eq_typ:str) -> list[Eqpment]:
        with open(self.EQM_FILE) as f:
            lines = f.readlines()

        eq_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            eq_id = line[0]
            name = line[1]
            eqtype = line[2]
            if eqtype.upper() == eq_typ.upper():
            
                eqmnt = Eqpment(eq_id,eqtype,name)
                eq_ls.append(eqmnt)
        
        return eq_ls

    def getWkp(self, wksh_id:str) -> Wrkshop:
        with open(self.WKS_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            c_wk_id = line[0]
            if wksh_id == c_wk_id:
                wk_name = line[1]
            
                wkshp = Wrkshop(wksh_id,wk_name)
                return wkshp
        
        return None                

    def getWkps(self,) -> list[Wrkshop]:
        with open(self.WKS_FILE) as f:
            lines = f.readlines()

        wksp_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")

            wksp_id = line[0]
            name = line[1]

            wkshop = Wrkshop(wksp_id,name)
            wksp_ls.append(wkshop)

        return wksp_ls

    def getTrns(self, dt_strt: str, dt_end: str) -> list[Trnsctn]:
        with open(self.TRN_FILE) as f:
            lines = f.readlines()

        trns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")

            trns_id = line[0]
            resv_id = line[1]
            desc = line[2]
            amount = float(line[3])
            billtyp = line[4]
            date = line[5]

            trnsctn = Trnsctn(trns_id,resv_id,desc,date,amount,billtyp)
            trns_ls.append(trnsctn)

        trns_cl = []
        dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        for trnsctn in trns_ls:
            date = datetime.strptime(trnsctn.date,'%m/%d/%Y').date()
            if dt_strt <= date and date <= dt_end:
                trns_cl.append(trnsctn)
        return trns_cl

    def getRvns(self, dt_strt: str, dt_end: str) -> list[Resrvtn]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            resv_id = line[0]
            cust_id = line[1]
            d_o_w = line[2]
            date_bk = line[3]
            date_rs = line[4]
            hr_strt = int(line[5])
            mm_strt = int(line[6])
            eq_id = line[7]
            wksp_id = line[8]
            canceld = bool(int(line[9]))
            
            rsvn = Resrvtn(resv_id,cust_id,date_bk,date_rs,d_o_w,hr_strt,mm_strt,canceld)
          
            if wksp_id != "":
                wkshop = self.getWkp(wksp_id)
                rsvn.add_wrk(wkshop)
            elif eq_id != "":
                eqpmnt = self.getEqmt(eq_id)
                rsvn.add_eqp(eqpmnt)

            rsvns_ls.append(rsvn)

        rvns_cl = []
        dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        for rsvn in rsvns_ls:
            date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
            if dt_strt <= date and date <= dt_end:
                rvns_cl.append(rsvn)

        return rvns_cl
    
    def getRvnC(self, cust_id:str, dt_strt: str, dt_end: str) -> list[Resrvtn]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            resv_id = line[0]
            ccst_id = line[1]
            d_o_w = line[2]
            date_bk = line[3]
            date_rs = line[4]
            hr_strt = int(line[5])
            mm_strt = int(line[6])
            eq_id = line[7]
            wksp_id = line[8]
            canceld = bool(int(line[9]))
            
            rsvn = Resrvtn(resv_id,ccst_id,date_bk,date_rs,d_o_w,hr_strt,mm_strt,canceld)

            if wksp_id != "":
                wkshop = self.getWkp(wksp_id)
                rsvn.add_wrk(wkshop)
            elif eq_id != "":
                eqpmnt = self.getEqmt(eq_id)
                rsvn.add_eqp(eqpmnt)

            if rsvn.custID == cust_id:
                rsvns_ls.append(rsvn)

        rvns_cl = []
        dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        for rsvn in rsvns_ls:
            date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
            if dt_strt <= date and date <= dt_end:
                rvns_cl.append(rsvn)

        return rvns_cl

    def nextRID(self) -> str:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        max_id = 0
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            cur_id = int(line[0])
            
            max_id = max(max_id, cur_id)

        return str(max_id + 1)

    def nextTID(self) -> str:
        with open(self.TRN_FILE) as f:
            lines = f.readlines()

        max_id = 0
        for line in lines:
            line = line.rstrip()
            line = line.split(",")           

            cur_id = int(line[0])
        
            max_id = max(max_id, cur_id)

        return str(max_id + 1)

    def saveRCl(self, rsvn: Resrvtn):
        """saves Reservation object after cancelling. this
        should only be run by cancel() subroutine. this will
        edit a line in resrvn.txt and possibly add lines to
        trnsctn.txt"""

        # implemented as:
        # (1) edit the canceld field in the rsrvtns.txt from 0 to 1 to indicate the reservation is canceled
        # (2) write the new transactions (refund transaction, if present) to the trnsctns.txt

        # (1)
        with open(self.RSV_FILE, "r+") as f:
            lines = f.readlines()
            
            for i,line in enumerate(lines):
                edtLine = line.rstrip()
                edtLine = edtLine.split(",")
                rsv_id = edtLine[0]
                
                if rsv_id == rsvn.resv_id:
                    edtLine[9] = "1"
                    updtdln = ",".join(edtLine)+"\n"
                    lines[i] = updtdln
                    break

            f.seek(0)
            f.truncate()
            f.writelines(lines)

        # (2)
        if rsvn.hasRfnd():
            rfnd = rsvn.getRef()

            with open(self.TRN_FILE, "a") as f:
                
                trns_id = rfnd.trns_id
                resv_id = rfnd.resv_id
                desc = rfnd.desc
                amount = '{:,.2f}'.format(rfnd.amnt)
                billtyp = rfnd.billtyp
                date = rfnd.date

                new_ln = ",".join([trns_id,resv_id,desc,amount,billtyp,date])

                f.write("\n")
                f.write(new_ln)
            
    def saveRnw(self, rsvn: Resrvtn):
        """saves Reservation object after creation. this
        should only be called by reserve() subroutine. this will
        write new lines to trnsctn.txt and to resrvn.txt"""

        # implemented as:
        # (1) add reservation to resrvn.txt
        # (2) add down payment transaction to trnsctn.txt

        # (1)
        with open(self.RSV_FILE, "a") as f:
            
            resv_id = rsvn.resv_id
            cust_id = rsvn.custID
            d_o_w = rsvn.d_o_w
            date_bk = rsvn.date_bk
            date_rs = rsvn.date_rs
            hr_strt = str(rsvn.hr_strt)
            mm_strt = str(rsvn.mm_strt)
            eq_id = rsvn.eqmnt.eq_id if rsvn.eqmnt is not None else ""
            wksp_id = rsvn.wrkshop.shop_id if rsvn.wrkshop is not None else ""
            canceld = "1" if rsvn.canceld else "0"

            new_ln = ",".join([resv_id,cust_id,d_o_w,date_bk,date_rs,hr_strt,mm_strt,eq_id,wksp_id,canceld])

            f.write("\n")
            f.write(new_ln)

        # (2)
        if rsvn.hasDwnP():
            trnsn = rsvn.getDwnP()

            with open(self.TRN_FILE, "a") as f:
                
                trns_id = trnsn.trns_id
                resv_id = trnsn.resv_id
                desc = trnsn.desc
                amount = '{:.2f}'.format(trnsn.amnt)
                billtyp = trnsn.billtyp
                date = trnsn.date

                new_ln = ",".join([trns_id,resv_id,desc,amount,billtyp,date])

                f.write("\n")
                f.write(new_ln)

    def getRwsp(self, wksp_id: str, dt_tm_st: datetime.date = None, dt_tm_en: datetime.date = None, rm_cncl: bool = True) -> list[Resrvtn]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            resv_id = line[0]
            cust_id = line[1]
            d_o_w = line[2]
            date_bk = line[3]
            date_rs = line[4]
            hr_strt = int(line[5])
            mm_strt = int(line[6])
            eq_id = line[7]
            c_wks_id = line[8]
            canceld = bool(int(line[9]))
            
            rsvn = Resrvtn(resv_id,cust_id,date_bk,date_rs,d_o_w,hr_strt,mm_strt,canceld)
          
            if c_wks_id != "":
                wkshop = self.getWkp(c_wks_id)
                rsvn.add_wrk(wkshop)
            elif eq_id != "":
                eqpmnt = self.getEqmt(eq_id)
                rsvn.add_eqp(eqpmnt)

            rsvns_ls.append(rsvn)

        # get all reservations for specific workshop id
        rvns_cl = []
        rsvn: Resrvtn
        for rsvn in rsvns_ls:
            if rsvn.wrkshop is not None:
                if rsvn.wrkshop.shop_id == wksp_id:
                    rvns_cl.append(rsvn)

        # filter by start date (also includes time)
        if dt_tm_st is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
                time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
                tm_st = datetime.combine(date,time)
                if dt_tm_st <= tm_st:
                    rvns_cl.append(rsvn)

        # filter by end date (Also includes time)
        if dt_tm_en is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
                time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
                tm_en = datetime.combine(date,time)
                if tm_en <= dt_tm_en:
                    rvns_cl.append(rsvn)

        # remove reservations that have been canceled (if specified)
        if rm_cncl:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if not rsvn.canceld:
                    rvns_cl.append(rsvn)

        return rvns_cl

    def getReqp(self, eq_id: str,  dt_tm_st: datetime.date = None, dt_tm_en: datetime.date = None, rm_cncl: bool = True) -> list[Resrvtn]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            resv_id = line[0]
            cust_id = line[1]
            d_o_w = line[2]
            date_bk = line[3]
            date_rs = line[4]
            hr_strt = int(line[5])
            mm_strt = int(line[6])
            c_eq_id = line[7]
            c_wks_id = line[8]
            canceld = bool(int(line[9]))
            
            rsvn = Resrvtn(resv_id,cust_id,date_bk,date_rs,d_o_w,hr_strt,mm_strt,canceld)
          
            if c_wks_id != "":
                wkshop = self.getWkp(c_wks_id)
                rsvn.add_wrk(wkshop)
            elif c_eq_id != "":
                eqpmnt = self.getEqmt(c_eq_id)
                rsvn.add_eqp(eqpmnt)

            rsvns_ls.append(rsvn)

        # get all reservations for specific eq id
        rvns_cl = []
        rsvn: Resrvtn
        for rsvn in rsvns_ls:
            if rsvn.eqmnt is not None:
                if rsvn.eqmnt.eq_id == eq_id:
                    rvns_cl.append(rsvn)

        # filter by start date (also includes time)
        if dt_tm_st is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
                time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
                tm_st = datetime.combine(date,time)
                if dt_tm_st <= tm_st:
                    rvns_cl.append(rsvn)

        # filter by end date (Also includes time)
        if dt_tm_en is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
                time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
                tm_en = datetime.combine(date,time)
                if tm_en <= dt_tm_en:
                    rvns_cl.append(rsvn)

        # remove reservations that have been canceled (if specified)
        if rm_cncl:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if not rsvn.canceld:
                    rvns_cl.append(rsvn)

        return rvns_cl

