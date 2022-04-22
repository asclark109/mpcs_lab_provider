"""module holding ObjRepo class. Responsible for creating objects from data in storage."""

# external
from __future__ import annotations
from datetime import datetime

# local
from bookable_item import BookableItem
from reservation import Reservation
from equipment import Equipment
from transaction import Transaction
from workshop import Workshop
from equipment_factory import EquipmentFactory

class ObjRepo():

    # should change this below so it works on other operating systems besides
    # windows. it may not work on linux because of the forward slash?
    DATA_PATH = "db/"
    TRN_FILE = DATA_PATH + "transactions.txt"
    RSV_FILE = DATA_PATH + "reservations.txt"
    WKS_FILE = DATA_PATH + "workshops.txt"
    EQM_FILE = DATA_PATH + "equipment.txt"

    def __init__(self) -> None:
        pass

    def get_equipment(self, eq_id:str) -> Equipment:
        with open(self.EQM_FILE) as f:
            lines = f.readlines()

        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            c_eq_id = line[0]
            if eq_id == c_eq_id:
                eq_name = line[1]
                eq_type = line[2]
                eqmnt = EquipmentFactory.create_equipment(eq_id,eq_type,eq_name)
                return eqmnt
        
        return None   

    def get_workshop(self, workshop_id:str) -> Workshop:
            with open(self.WKS_FILE) as f:
                lines = f.readlines()

            rsvns_ls = []
            for line in lines:
                line = line.rstrip()
                line = line.split(",")
            
                if workshop_id == line[0]:
                    workshop_name = line[1]
                
                    workshop = Workshop(workshop_id,workshop_name)
                    return workshop
            
            return None          

    def get_reservation(self, rsvn_id:str) -> Reservation:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            c_rv_id = line[0]
            if rsvn_id == c_rv_id:
                # unpack data
                cust_id = line[1]
                # d_o_w = line[2]
                date_bk = line[2]
                date_rs = line[3]
                hr_strt = int(line[4])
                mm_strt = int(line[5])
                duration = float(line[6])
                eq_id = line[7]
                wksp_id = line[8]
                canceld = bool(int(line[9]))

                # make datetime for start time
                date_booked = datetime.strptime(date_bk, "%m/%d/%Y")
                # make datetime for start time
                date_rs = line[3]
                hr_strt = line[4]
                mm_strt = line[5]
                date_str = "{} {}:{}".format(date_rs,hr_strt,mm_strt)
                date_reserv = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
                
                # generate booked item
                if wksp_id != "":
                    bookable_item: BookableItem = self.get_workshop(wksp_id)
                elif eq_id != "":
                    bookable_item: BookableItem = self.get_equipment(eq_id)

                # create reservation
                rsvn = Reservation(rsvn_id, cust_id, date_booked, date_reserv, bookable_item, duration, canceld)
                
                return rsvn
        
        return None

    def get_equipment_by_type(self, eq_type:str) -> list[Equipment]:
        """eq_type should be one of {Micrvac,Irradtr,PlymExt,HiVelCr,LiHrvst}"""
        with open(self.EQM_FILE) as f:
            lines = f.readlines()

        # find all equipment ID's with the equipment type specified
        eq_ids = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            eq_id = line[0]
            name = line[1]
            eqtype = line[2]
            if eqtype.upper() == eq_type.upper():
            
                eq_ids.append(eq_id)
                
        # for each equipment ID, make an Equipment object and append to a list
        eq_list = []
        for id in eq_ids:
            equipment_obj = self.get_equipment(id)
            eq_list.append(equipment_obj)
        
        return eq_list

    def get_workshops(self) -> list[Workshop]:
        with open(self.WKS_FILE) as f:
            lines = f.readlines()

        wksp_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")

            wksp_id = line[0]
            name = line[1]

            wkshop = Workshop(wksp_id,name)
            wksp_ls.append(wkshop)

        return wksp_ls

    def get_transactions(self, dt_strt: str, dt_end: str) -> list[Transaction]:
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

            trnsctn = Transaction(trns_id,resv_id,desc,date,amount,billtyp)
            trns_ls.append(trnsctn)

        trns_cl = []
        dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        for trnsctn in trns_ls:
            date = datetime.strptime(trnsctn.date,'%m/%d/%Y').date()
            if dt_strt <= date and date <= dt_end:
                trns_cl.append(trnsctn)
        return trns_cl

    def get_reservations_by_date(self, dt_strt: str, dt_end: str) -> list[Reservation]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            # unpack data
            rsvn_id = line[0]
            cust_id = line[1]
            # d_o_w = line[2]
            date_bk = line[2]
            date_rs = line[3]
            hr_strt = int(line[4])
            mm_strt = int(line[5])
            duration = float(line[6])
            eq_id = line[7]
            wksp_id = line[8]
            canceld = bool(int(line[9]))

            # make datetime for start time
            date_booked = datetime.strptime(date_bk, "%m/%d/%Y")
            # make datetime for start time
            date_rs = line[3]
            hr_strt = line[4]
            mm_strt = line[5]
            date_str = "{} {}:{}".format(date_rs,hr_strt,mm_strt)
            date_reserv = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
            
            # generate booked item
            if wksp_id != "":
                bookable_item: BookableItem = self.get_workshop(wksp_id)
            elif eq_id != "":
                bookable_item: BookableItem = self.get_equipment(eq_id)

            # create reservation
            rsvn = Reservation(rsvn_id, cust_id, date_booked, date_reserv, bookable_item, duration, canceld)
            
            rsvns_ls.append(rsvn)

        rvns_cl = []
        dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        rsvn: Reservation
        for rsvn in rsvns_ls:
            date = rsvn.start_datetime.date()
            if dt_strt <= date and date <= dt_end:
                rvns_cl.append(rsvn)

        return rvns_cl
    
    def get_reservations_by_custID(self, query_cust_id:str, dt_strt: str, dt_end: str) -> list[Reservation]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            # unpack data
            rsvn_id = line[0]
            cust_id = line[1]
            # d_o_w = line[2]
            date_bk = line[2]
            date_rs = line[3]
            hr_strt = int(line[4])
            mm_strt = int(line[5])
            duration = float(line[6])
            eq_id = line[7]
            wksp_id = line[8]
            canceld = bool(int(line[9]))

            # make datetime for start time
            date_booked = datetime.strptime(date_bk, "%m/%d/%Y")
            # make datetime for start time
            date_rs = line[3]
            hr_strt = line[4]
            mm_strt = line[5]
            date_str = "{} {}:{}".format(date_rs,hr_strt,mm_strt)
            date_reserv = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
            
            # generate booked item
            if wksp_id != "":
                bookable_item: BookableItem = self.get_workshop(wksp_id)
            elif eq_id != "":
                bookable_item: BookableItem = self.get_equipment(eq_id)

            # create reservation
            rsvn = Reservation(rsvn_id, cust_id, date_booked, date_reserv, bookable_item, duration, canceld)
            
            # only add reservation to list of candidate reservations
            # if it matches customer id
            if rsvn.custID == query_cust_id:
                rsvns_ls.append(rsvn)

        rvns_cl = []
        dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        rsvn: Reservation
        for rsvn in rsvns_ls:
            date = rsvn.start_datetime.date()
            if dt_strt <= date and date <= dt_end:
                rvns_cl.append(rsvn)

        return rvns_cl
        
    def next_reservation_ID(self) -> str:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        max_id = 0
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            cur_id = int(line[0])
            
            max_id = max(max_id, cur_id)

        return str(max_id + 1)

    def next_transaction_ID(self) -> str:
        with open(self.TRN_FILE) as f:
            lines = f.readlines()

        max_id = 0
        for line in lines:
            line = line.rstrip()
            line = line.split(",")           

            cur_id = int(line[0])
        
            max_id = max(max_id, cur_id)

        return str(max_id + 1)

    def save_canceled_reservation(self, canceled_rsvn: Reservation):
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
                
                if rsv_id == canceled_rsvn.resv_id:
                    edtLine[9] = "1"
                    updtdln = ",".join(edtLine)+"\n"
                    lines[i] = updtdln
                    break

            f.seek(0)
            f.truncate()
            f.writelines(lines)

        # (2)
        if canceled_rsvn.has_refund():
            rfnd = canceled_rsvn.get_refund()

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
 
    def save_new_reservation(self, new_rsvn: Reservation):
        """saves Reservation object after creation. this
        should only be called by reserve() subroutine. this will
        write new lines to trnsctn.txt and to resrvn.txt"""

        # implemented as:
        # (1) add reservation to resrvn.txt
        # (2) add down payment transaction to trnsctn.txt

        # (1)
        with open(self.RSV_FILE, "a") as f:
            
            resv_id = new_rsvn.resv_id
            cust_id = new_rsvn.custID
            # d_o_w = new_rsvn.d_o_w
            date_bk = new_rsvn.time_of_creation_datetime.date().strftime("%m/%d/%Y")
            date_rs = new_rsvn.start_datetime.date().strftime("%m/%d/%Y")
            hr_strt = str(new_rsvn.start_datetime.hour)
            mm_strt = str(new_rsvn.start_datetime.minute)
            duration = str(new_rsvn.duration)
            # hr_strt = str(new_rsvn.hr_strt)
            # mm_strt = str(new_rsvn.mm_strt)
            if isinstance(new_rsvn.bookable_item,Workshop):
                wksp_id = new_rsvn.bookable_item.shop_id
                eq_id = ""
            elif isinstance(new_rsvn.bookable_item,Equipment):
                wksp_id = ""
                eq_id = new_rsvn.bookable_item.eq_id
            canceld = "1" if new_rsvn.canceld else "0"

            new_ln = ",".join([resv_id,cust_id,date_bk,date_rs,hr_strt,mm_strt,duration,eq_id,wksp_id,canceld])

            f.write("\n")
            f.write(new_ln)

        # (2)
        if new_rsvn.has_downpayment():
            trnsn = new_rsvn.get_downpayment()

            with open(self.TRN_FILE, "a") as f:
                
                trns_id = trnsn.trns_id
                resv_id = trnsn.resv_id
                desc = trnsn.desc
                amount = '{:.2f}'.format(trnsn.amnt)
                billtyp = trnsn.billtyp
                date = trnsn.date.strftime("%m/%d/%Y")

                new_ln = ",".join([trns_id,resv_id,desc,amount,billtyp,date])

                f.write("\n")
                f.write(new_ln)

    def get_reservations_by_wkshop_id(self, query_workshop_id: str, dt_tm_st: datetime = None, dt_tm_en: datetime = None, exclude_canceled_reservations: bool = True) -> list[Reservation]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            # unpack data
            rsvn_id = line[0]
            cust_id = line[1]
            # d_o_w = line[2]
            date_bk = line[2]
            date_rs = line[3]
            hr_strt = int(line[4])
            mm_strt = int(line[5])
            duration = float(line[6])
            eq_id = line[7]
            wksp_id = line[8]
            canceld = bool(int(line[9]))

            # make datetime for start time
            date_booked = datetime.strptime(date_bk, "%m/%d/%Y")
            # make datetime for start time
            date_rs = line[3]
            hr_strt = line[4]
            mm_strt = line[5]
            date_str = "{} {}:{}".format(date_rs,hr_strt,mm_strt)
            date_reserv = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
            
            # if booked item is a workshop, add this reservation to list
            if wksp_id != "":
                bookable_item: BookableItem = self.get_workshop(wksp_id)    
                # create reservation
                rsvn = Reservation(rsvn_id, cust_id, date_booked, date_reserv, bookable_item, duration, canceld)
                rsvns_ls.append(rsvn)

        # get all reservations for specific workshop id
        rvns_cl = []
        rsvn: Reservation
        for rsvn in rsvns_ls:
            if rsvn.bookable_item.get_id() == query_workshop_id:
                rvns_cl.append(rsvn)


        # dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        # dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        # rsvn: Reservation
        # for rsvn in rsvns_ls:
        #     date = rsvn.start_datetime.date()
        #     if dt_strt <= date and date <= dt_end:
        #         rvns_cl.append(rsvn)

        # filter by start date (also includes time)
        if dt_tm_st is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if dt_tm_st <= rsvn.start_datetime:
                    rvns_cl.append(rsvn)
                # date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
                # time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
                # tm_st = datetime.combine(date,time)
                # if dt_tm_st <= tm_st:
                #     rvns_cl.append(rsvn)

        # filter by end date (Also includes time)
        if dt_tm_en is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if rsvn.end_datetime <= dt_tm_en:
                    rvns_cl.append(rsvn)
            # for rsvn in tmp_ls:
            #     date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
            #     time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
            #     tm_en = datetime.combine(date,time)
            #     if tm_en <= dt_tm_en:
            #         rvns_cl.append(rsvn)

        # remove reservations that have been canceled (if specified)
        if exclude_canceled_reservations:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if not rsvn.canceld:
                    rvns_cl.append(rsvn)

        return rvns_cl

    def get_reservations_by_eq_id(self, query_eq_id: str,  dt_tm_st: datetime = None, dt_tm_en: datetime = None, exclude_canceled_reservations: bool = True) -> list[Reservation]:
        with open(self.RSV_FILE) as f:
            lines = f.readlines()

        rsvns_ls = []
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
        
            # unpack data
            rsvn_id = line[0]
            cust_id = line[1]
            # d_o_w = line[2]
            date_bk = line[2]
            date_rs = line[3]
            hr_strt = int(line[4])
            mm_strt = int(line[5])
            duration = float(line[6])
            eq_id = line[7]
            wksp_id = line[8]
            canceld = bool(int(line[9]))

            # make datetime for start time
            date_booked = datetime.strptime(date_bk, "%m/%d/%Y")
            # make datetime for start time
            date_rs = line[3]
            hr_strt = line[4]
            mm_strt = line[5]
            date_str = "{} {}:{}".format(date_rs,hr_strt,mm_strt)
            date_reserv = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
            
            # if booked item is a workshop, add this reservation to list
            if eq_id != "":
                bookable_item: BookableItem = self.get_equipment(eq_id)    
                # create reservation
                rsvn = Reservation(rsvn_id, cust_id, date_booked, date_reserv, bookable_item, duration, canceld)
                rsvns_ls.append(rsvn)

        # get all reservations for specific workshop id
        rvns_cl = []
        rsvn: Reservation
        for rsvn in rsvns_ls:
            if rsvn.bookable_item.get_id() == query_eq_id:
                rvns_cl.append(rsvn)


        # dt_strt = datetime.strptime(dt_strt, '%m/%d/%Y').date()
        # dt_end = datetime.strptime(dt_end, '%m/%d/%Y').date()
        # rsvn: Reservation
        # for rsvn in rsvns_ls:
        #     date = rsvn.start_datetime.date()
        #     if dt_strt <= date and date <= dt_end:
        #         rvns_cl.append(rsvn)

        # filter by start date (also includes time)
        if dt_tm_st is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if dt_tm_st <= rsvn.start_datetime:
                    rvns_cl.append(rsvn)
                # date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
                # time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
                # tm_st = datetime.combine(date,time)
                # if dt_tm_st <= tm_st:
                #     rvns_cl.append(rsvn)

        # filter by end date (Also includes time)
        if dt_tm_en is not None:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if rsvn.end_datetime <= dt_tm_en:
                    rvns_cl.append(rsvn)
            # for rsvn in tmp_ls:
            #     date = datetime.strptime(rsvn.date_rs,'%m/%d/%Y').date()
            #     time = datetime.strptime("{}:{}".format(rsvn.hr_strt,rsvn.mm_strt),"%H:%M").time()
            #     tm_en = datetime.combine(date,time)
            #     if tm_en <= dt_tm_en:
            #         rvns_cl.append(rsvn)

        # remove reservations that have been canceled (if specified)
        if exclude_canceled_reservations:
            tmp_ls = rvns_cl.copy()
            rvns_cl = []
            for rsvn in tmp_ls:
                if not rsvn.canceld:
                    rvns_cl.append(rsvn)

        return rvns_cl


def main():
    """use this method to play around with repository"""
    repo = ObjRepo()
    # eqpmnt_list = repo.get_equipment_by_type("Micrvac")
    # print(eqpmnt_list)

    # workshops = repo.get_workshops()
    # print(workshops)

    # result = repo.get_reservations_by_date("4/3/2022","4/4/2022")
    # print(result)

    # result = repo.get_reservations_by_custID("1","4/3/2022","4/4/2022")
    # print(result)

    dt_st = datetime.strptime("4/2/2022 10:01",'%m/%d/%Y %H:%M')
    dt_end = datetime.strptime("4/4/2022 23:59",'%m/%d/%Y %H:%M')

    # result = repo.get_reservations_by_wkshop_id("1")
    # for res in result:
    #     print(res)

    result = repo.get_reservations_by_eq_id("1",dt_tm_st=dt_st,dt_tm_en=dt_end) #dt_st,dt_end
    for res in result:
        print(res)

    #     get_reservations_by_eq_id
    
if __name__ == "__main__":
    main()
