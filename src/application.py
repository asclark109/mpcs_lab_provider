from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta

from reservation import Reservation
from equipment import Equipment
from transaction import Transaction
from repository import ObjRepo
from workshop import Workshop

##### domain code (APP) ######

class Application():

    def reserve(self,custID: str, rsvType: str, date_rs:str, hr_strt:str, mm_strt:str, duration:float, save: bool = False):

        # generate datetime representations of start and end of reservation
        datetime_str = "{} {}:{}".format(date_rs,hr_strt,mm_strt)
        reservation_start_datetime = datetime.strptime(datetime_str,'%m/%d/%Y %H:%M')
        reservation_end_datetime = reservation_start_datetime + timedelta(hours = duration)

        # (0) determine weekday
        d_o_w = self._datetime_to_weekday_str(reservation_start_datetime)

        # (0) confirm reservation is 30 days within today
        print("checking date window for booking reservation...")
        now_datetime = datetime.now()
        today_date = now_datetime.date()
        delta = reservation_start_datetime.date() - today_date
        if delta.days > 30:
            print("Fail. cant reserve more than 30 days into future.")
            return

        # (0) confirm business is open
        print("checking business hours...")
        if not self._is_business_open_for_window(d_o_w,reservation_start_datetime, reservation_end_datetime):
            print("Fail. business is not open at this time")
            return

        # reserve a workshop
        if rsvType.upper() == "WRKSHOP":
            self._reserve_workshop(custID,now_datetime,reservation_start_datetime,reservation_end_datetime,duration,save)

        # reserve a piece of equipment
        elif rsvType.upper() in ["MICRVAC", "IRRADTR", "PLYMEXT", "HIVELCR", "LIHRVST"]:
            self._reserve_equipment(custID,now_datetime,reservation_start_datetime,reservation_end_datetime,duration,rsvType,save)

        else:
            print("Fail. Did not recognize reservation type. must be one of ['WRKSHOP','MICRVAC','IRRADTR','PLYMEXT','HIVELCR','LIHRVST']")
            return

    def cancel(self,custID: str, rsrvID: str, save: bool = True):
        """assumes reservation is not already canceled"""

        print("\ncancelling reservation id={} for customer id={}.".format(rsrvID,custID))

        # fetch existing reservation
        repo = ObjRepo()
        rsvn = repo.get_reservation(rsrvID)

        # (0) calculate refund
        subtotal = rsvn.calc_tot_cost()
        print("subtotal: ",subtotal)

        downpayment = rsvn.calc_downpayment()
        print("downpayment (50pcnt subtotal): ",downpayment)

        refund = rsvn.calc_refund()
        print("refund: ",refund)

        # (1) cancel the reservation
        rsvn.cancel()

        # if the refund is non-zero, create a refund transaction and
        # add it to the reservation
        if refund != 0:
            new_TID = repo.next_transaction_ID()
            today = date.today()
            trnsctn = Transaction(new_TID, rsrvID, "refund (cancellation)",today,refund,"DEBIT")
            print("adding refund to list of transactions...")
            rsvn.add_transaction(trnsctn)

        # save reservation (write new line to text file) and 
        # save new transaction (down payment, if present, to text file)
        if save:
            print("saving changes...")
            repo.save_canceled_reservation(rsvn)        

    def view_report(self,dt_strt: str, dt_end: str):
        print("\nviewing report: reservations by date.")

        # get reservations by date
        repo = ObjRepo()
        rvns_list = repo.get_reservations_by_date(dt_strt,dt_end)

        
        # print out results
        headers = ["resv id","date booked", "date resrvd", "start", "end", "customer id", "equipment id","name", "workshop id", "name", "status"]
        header_str = "   ".join(headers)
        to_print = []
        to_print.append(headers)

        headers = ["-------","-----------", "-----------", "------","---", "-----------", "------------","----", "-----------", "----", "------"]
        header_str = "   ".join(headers)
        to_print.append(headers)
        
        for rvn in rvns_list:
            resv_id = rvn.resv_id
            date_bk = rvn.time_of_creation_datetime.date().strftime('%m/%d/%Y') # mm/dd/yyyy as str
            date_rs = rvn.start_datetime.date().strftime('%m/%d/%Y') # mm/dd/yyyy as str
            custID = rvn.custID
            if isinstance(rvn.bookable_item,Workshop):
                eqmntID = "-"
                eqmntNM = "-"
                wkshpID = rvn.bookable_item.get_id()
                wkshpNM = rvn.bookable_item.get_name()
            elif isinstance(rvn.bookable_item,Equipment):
                eqmntID = rvn.bookable_item.get_id()
                eqmntNM = rvn.bookable_item.get_name()
                wkshpID = "-"
                wkshpNM = "-"
            else:
                raise Exception("fatal error. Reservation did not have a bookable item")
            canceld = "CANCELED" if rvn.canceld else "ACTIVE"


            hr_strt = rvn.start_datetime.hour
            mm_strt = rvn.start_datetime.minute
            hr_end = rvn.end_datetime.hour
            mm_end = rvn.end_datetime.minute

            if hr_strt > 12:
                hr_strt -= 12
                st_ampm = " pm"
            else:
                st_ampm = " am"            

            if hr_end > 12:
                hr_end -= 12
                en_ampm = " pm"
            else:
                en_ampm = " am"

            time_st = str(hr_strt)+":"+str(mm_strt).zfill(2)+st_ampm
            time_en = str(hr_end)+":"+str(mm_end).zfill(2)+en_ampm

            values = [resv_id,date_bk, date_rs,time_st,time_en,custID,eqmntID,eqmntNM,wkshpID,wkshpNM,canceld]
            to_print.append(values)

        # calculate the character width of every str to be printed out,
        # and calculate the minimum amount of space needed to fit all strs
        # in each column
        elmLens = [list(map(len,item)) for item in to_print]
        col_wds = list(map(list, zip(*elmLens)))
        max_c_w = [max(width) for width in col_wds]

        # print out the list of lists, padding each string with the right amount of blank space
        all_rep = ''
        for row in to_print:
            for idx,elem in enumerate(row):
                all_rep += elem.ljust(max_c_w[idx] + 2)
            all_rep += "\n"

        print(all_rep)
        
    def view_transactions(self,dt_strt: str, dt_end: str):
        print("\nviewing transactions: transactions by date.")

        # fetch transactions
        repo = ObjRepo()
        trns_list = repo.get_transactions(dt_strt,dt_end)

        # display results
        headers = ["date", "transaction id","resv id", "type", "desc", "amount"]
        header_str = "   ".join(headers)
        to_print = []
        to_print.append(headers)

        headers = ["----", "--------------","-------", "----", "----", "------"]
        header_str = "   ".join(headers)
        to_print.append(headers)

        trnsctn: Transaction
        for trnsctn in trns_list:
            date = trnsctn.date # mm/dd/yyyy as str
            trns_id = trnsctn.trns_id
            resv_id = trnsctn.resv_id
            billtyp = trnsctn.billtyp
            desc = trnsctn.desc
            amount = trnsctn.amnt

            amt_str = '${:,.2f}'.format(amount)
            amt_str = "+"+amt_str if billtyp == "CREDIT" else "-"+amt_str

            values = [date,trns_id,resv_id,billtyp,desc,amt_str]
            to_print.append(values)

        # calculate the character width of every str to be printed out,
        # and calculate the minimum amount of space needed to fit all strs
        # in each column
        elmLens = [list(map(len,item)) for item in to_print]
        col_wds = list(map(list, zip(*elmLens)))
        max_c_w = [max(width) for width in col_wds]

        # print out the list of lists, padding each string with the right amount of blank space
        all_rep = ''
        for row in to_print:
            for idx,elem in enumerate(row):
                all_rep += elem.ljust(max_c_w[idx] + 2)
            all_rep += "\n"

        print(all_rep)

    def view_reservations(self,custID: str, dt_strt: str, dt_end: str):

        print("\nviewing reservations: reservations by date, customer ID.")
        
        # fetch reservations by customer id
        repo = ObjRepo()
        rvns_list = repo.get_reservations_by_custID(custID,dt_strt,dt_end)

        # print out results
        headers = ["resv id","date booked", "date resrvd", "start", "end", "customer id", "equipment id","name", "workshop id", "name", "status"]
        header_str = "   ".join(headers)
        to_print = []
        to_print.append(headers)

        headers = ["-------","-----------", "-----------", "------","---", "-----------", "------------","----", "-----------", "----", "------"]
        header_str = "   ".join(headers)
        to_print.append(headers)
        
        for rvn in rvns_list:
            resv_id = rvn.resv_id
            date_bk = rvn.time_of_creation_datetime.date().strftime('%m/%d/%Y') # mm/dd/yyyy as str
            date_rs = rvn.start_datetime.date().strftime('%m/%d/%Y') # mm/dd/yyyy as str
            custID = rvn.custID
            if isinstance(rvn.bookable_item,Workshop):
                eqmntID = "-"
                eqmntNM = "-"
                wkshpID = rvn.bookable_item.get_id()
                wkshpNM = rvn.bookable_item.get_name()
            elif isinstance(rvn.bookable_item,Equipment):
                eqmntID = rvn.bookable_item.get_id()
                eqmntNM = rvn.bookable_item.get_name()
                wkshpID = "-"
                wkshpNM = "-"
            else:
                raise Exception("fatal error. Reservation did not have a bookable item")
            canceld = "CANCELED" if rvn.canceld else "ACTIVE"


            hr_strt = rvn.start_datetime.hour
            mm_strt = rvn.start_datetime.minute
            hr_end = rvn.end_datetime.hour
            mm_end = rvn.end_datetime.minute

            if hr_strt > 12:
                hr_strt -= 12
                st_ampm = " pm"
            else:
                st_ampm = " am"            

            if hr_end > 12:
                hr_end -= 12
                en_ampm = " pm"
            else:
                en_ampm = " am"

            time_st = str(hr_strt)+":"+str(mm_strt).zfill(2)+st_ampm
            time_en = str(hr_end)+":"+str(mm_end).zfill(2)+en_ampm

            values = [resv_id,date_bk, date_rs,time_st,time_en,custID,eqmntID,eqmntNM,wkshpID,wkshpNM,canceld]
            to_print.append(values)

        # calculate the character width of every str to be printed out,
        # and calculate the minimum amount of space needed to fit all strs
        # in each column
        elmLens = [list(map(len,item)) for item in to_print]
        col_wds = list(map(list, zip(*elmLens)))
        max_c_w = [max(width) for width in col_wds]

        # print out the list of lists, padding each string with the right amount of blank space
        all_rep = ''
        for row in to_print:
            for idx,elem in enumerate(row):
                all_rep += elem.ljust(max_c_w[idx] + 2)
            all_rep += "\n"

        print(all_rep)

    def _is_business_open_for_window(self, d_o_w: str, reservation_start: datetime, reservation_end:datetime)->bool:
        """returns true if business is open for the reservation duration"""

        WEEKDAY_HR_START = 9
        WEEKDAY_HR_END = 12+6
        SAT_HR_START = 10
        SAT_HR_END = 12+4

        if d_o_w.upper() in ["MON","TUES","WED","THRS","FRI"]:
            if reservation_start.hour < WEEKDAY_HR_START:
                print(reservation_start.hour,"less than",WEEKDAY_HR_START)
                return False
            if reservation_end.hour == WEEKDAY_HR_END:
                if reservation_end.minute != 0:
                    print("HERE!!!")
                    return False

        if d_o_w.upper() in ["SAT"]:
            if reservation_start.hour < SAT_HR_START:
                print(reservation_start.hour,"less than",SAT_HR_START)
                return False
            if reservation_end.hour == SAT_HR_END:
                if reservation_end.minute != 0:
                    print("HERE!!!")
                    return False    

        if d_o_w.upper() in ["SUN"]:
            print("not open on sunday")
            return False

        return True 

    def _datetime_to_weekday_str(self, datetime_obj: datetime)->str:
        """returns one of {'MON','TUES','WED','THRS','FRI','SAT','SUN'}"""
        day_int = datetime_obj.weekday()
        day_map = {
            0:"MON",
            1:"TUES",
            2:"WED",
            3:"THRS",
            4:"FRI",
            5:"SAT",
            6:"SUN"
        }
        d_o_w = day_map[day_int]
        return d_o_w

    def _reserve_workshop(self,custID: str, booking_date_datetime: datetime, reservation_start_datetime:datetime,reservation_end_datetime:datetime, duration:float, save:bool):
        print("attempting to book workshop...")
        # attempt to book a workshop appointment

        # (1) find available workshops

        # get workshops
        objrepo = ObjRepo()
        workshop_list = objrepo.get_workshops()

        # for each workshop, get the reservations
        # associated with that workshop on that day and check if
        # none of them time conflict with the to-be-created 
        # reservation. If none of them conflict, then that
        # workshop is available at the reservation window.
        found_workshop = False
        for workshop in workshop_list:
            workshop_id = workshop.shop_id
            day_of = reservation_start_datetime.date()
            start_of_day_time = datetime.strptime('00:00', '%H:%M').time()
            end_of_day_time = datetime.strptime('23:59', '%H:%M').time()
            start_of_day = datetime.combine(day_of, start_of_day_time)
            end_of_day = datetime.combine(day_of, end_of_day_time)

            # fetch all reservations for this workshop id on the day of this reservation
            rsvn_ls = objrepo.get_reservations_by_wkshop_id(workshop_id,start_of_day,end_of_day)

            # remove reservations that do not conflict
            conflicting_reservations = [rsvn for rsvn in rsvn_ls if rsvn.overlaps_with_window(reservation_start_datetime,reservation_end_datetime)]

            if len(conflicting_reservations) == 0:
                print("workshop available!: id={}".format(workshop_id))
                found_workshop = True
                workshop_to_book = workshop
                break
            else:
                # print(workshop_id)
                print("workshop already booked!: id={}".format(workshop_id))

        if not found_workshop:
            print("Fail. did not find available workshop at this time.")
            return

        # (2) create the new Reservation object in memory.
        # it will only become official when we save it to memory
        print("creating reservation...")
        objrepo = ObjRepo()
        new_rsvn_id = objrepo.next_reservation_ID()
        # today = date.today().strftime("%m/%d/%Y")
        new_rvn = Reservation(new_rsvn_id,custID,booking_date_datetime,reservation_start_datetime,workshop_to_book,duration)
        # new_rvn.add_wrk(wkshp_b)
        print("created reservation: {}".format(new_rvn))

        
        # (3) calculate reservation costs, discounts, downpayment
        print("calculating total cost")
        total_cost = new_rvn.calc_tot_cost()
        print('${:,.2f}'.format(total_cost))

        print("calculating discount")
        discount = new_rvn.calc_discount(total_cost)
        print('${:,.2f}'.format(discount))

        print("calculating subtotal (total cost - discount)")
        subtotal = total_cost - discount
        print('${:,.2f}'.format(subtotal))
        
        print("calculating downpayment")
        dnpymt = new_rvn.calc_downpayment()
        print('${:,.2f}'.format(dnpymt))

        # (4) add transactions to list of transactions for reservation 
        # adding any new transactions to reservation
        # for now, only downpayment, if there is one,
        # but for reservations there is no downpayment.
        new_trns_ID = objrepo.next_transaction_ID()
        if dnpymt > 0:
            tdy = booking_date_datetime.day
            new_trns = Transaction(new_trns_ID,new_rvn.resv_id,r"50% down payment",tdy,dnpymt,"CREDIT")
            print("adding downpayment to the reservation's list of transactions...")
            new_rvn.add_transaction(new_trns)

        # assert new_rvn.hasDwnP() == False

        # (5) save changes (newly created reservation)
        if save:
            print("saving changes...")
            objrepo.save_new_reservation(new_rvn)

    def _reserve_equipment(self,custID: str, booking_date_datetime: datetime, reservation_start_datetime:datetime,reservation_end_datetime:datetime, duration:float,rsvType:str, save:bool):
        eq_nms = {
            "MICRVAC": "Mini Microvac",
            "IRRADTR": "Irradiator",
            "PLYMEXT": "Polymer Extruder",
            "HIVELCR": "High Velocity Crusher",
            "LIHRVST": "1.21 Gigawatt Lightning Harvester",
        }

        # attempt to book a piece of equipment
        print("attempting to book piece of equipment: {}...".format(eq_nms[rsvType.upper()]))
        
        # (1) find available equipment

        # get list of equipment that all have the specified type
        objrepo = ObjRepo()
        eq_ls = objrepo.get_equipment_by_type(rsvType)

        # for each piece of equipment, get the reservations
        # associated with that piece of equipment at the 
        # to-be-desired reservation time (i.e. all reservations
        # within some time window). if reservation list empty, 
        # we found a piece of equipment that is not booked for
        # that period of time. Else, if we've looked at every 
        # piece of equipment corresponding to that equipment type,
        # then that equipment type is fully booked. 
        # (additionally, other special considerations are made
        # for certain types of equipment. e.g. for high velocity
        # crusher, we check a larger window of time (we look at
        # the 6 hr, 30 min block of time beginning at the desired
        # reservation time to ensure we allow a 6 hr cooldown --
        # since worst case scenario a client uses the machine at
        # the last second of their 30 minute window booking, meaning
        # we need 6 hours after the end of their reservation to
        # recalibrate the machine)

        fnd_eqt = False
        eqpmnt: Equipment
        for eqpmnt in eq_ls:
            eq_id = eqpmnt.eq_id
            # if handling high velocity crusher, we need to confirm there is no
            # additional high velocity crusher reservation 6 hours prior to 
            # desired reservation time, and we need to look 6 hours and 30 minutes
            # past desired reservation time to confirm there is not an existing
            # high velocity crusher reservation. this ensurees there is enough 
            # buffer time for recalibration.
            if rsvType.upper() == "HIVELCR":
                # # left bounded time
                # dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
                # time = datetime.strptime("{}:{}".format(int(hr_strt),str(mm_strt).zfill(2)),"%H:%M").time()   
                # dt_st = datetime.combine(dt,time)
                # decrement by 5 hours 59 minutes
                dt_st_B = reservation_start_datetime - timedelta(hours=5,minutes=59)

                # right bounded time
                # if mm_strt == 0:
                #     hr_end = int(hr_strt) + 6
                #     mm_end = 30
                # else:
                #     hr_end = int(hr_strt) + 6 + 1
                #     mm_end = 0
                # time = datetime.strptime("{}:{}".format(hr_end,str(mm_end).zfill(2)),"%H:%M").time()   
                dt_en = reservation_start_datetime
                # increment by 6 hours + duration time
                dt_en_B = dt_en + timedelta(hours=6) + timedelta(hours=duration)
                print(dt_st_B,dt_en_B)
            else:
                # dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
                # time = datetime.strptime("{}:{}".format(hr_strt,str(mm_strt).zfill(2)),"%H:%M").time()   
                dt_st_B = reservation_start_datetime
                dt_en_B = reservation_end_datetime


            day_of = reservation_start_datetime.date()
            start_of_day_time = datetime.strptime('00:00', '%H:%M').time()
            end_of_day_time = datetime.strptime('23:59', '%H:%M').time()
            start_of_day = datetime.combine(day_of, start_of_day_time)
            end_of_day = datetime.combine(day_of, end_of_day_time)

            # fetch all reservations for this equipment id on the day of this reservation
            rsvn_ls = objrepo.get_reservations_by_eq_id(eq_id,start_of_day,end_of_day)

            # look for conflicting reservations
            conflicting_reservations = [rsvn for rsvn in rsvn_ls if rsvn.overlaps_with_window(dt_st_B,dt_en_B)]

            if len(conflicting_reservations) == 0:
                print("{} available!: id={}".format(eqpmnt.eq_name,eq_id))
                fnd_eqt = True
                equipment_to_book = eqpmnt
                break
            else:
                # print(wksp_id)
                print("{} booked!: id={}".format(eqpmnt.eq_name,eq_id))

        if not fnd_eqt:
            print("Fail. did not find available {} at this time.".format(eq_nms[rsvType.upper()]))
            return

        # (2) create piece of equipment reservation

        # create reservation for this time for this piece of equipment
        # print("creating reservation...")
        # newID = objrepo.next_reservation_ID()
        # tdy = date.today().strftime("%m/%d/%Y")
        # new_rvn = Resrvtn(newID,custID,tdy,date_rs,d_o_w,hr_strt,mm_strt)
        # new_rvn.add_eqp(eqmnt_b)
        # print("created reservation: {}".format(new_rvn))

        # (2) create piece of equipment reservation
        # create reservation for this time for this piece of equipment
        # it will only become official when we save it to memory
        print("creating reservation...")
        objrepo = ObjRepo()
        new_rsvn_id = objrepo.next_reservation_ID()
        # today = date.today().strftime("%m/%d/%Y")
        new_rvn = Reservation(new_rsvn_id,custID,booking_date_datetime,reservation_start_datetime,equipment_to_book,duration)
        # new_rvn.add_wrk(wkshp_b)
        print("created reservation: {}".format(new_rvn))

        # (3) calculate reservation costs, discounts, downpayment
        print("calculating total cost")
        total_cost = new_rvn.calc_tot_cost()
        print('${:,.2f}'.format(total_cost))

        print("calculating discount")
        discount = new_rvn.calc_discount(total_cost)
        print('${:,.2f}'.format(discount))

        print("calculating subtotal (total cost - discount)")
        subtotal = total_cost - discount
        print('${:,.2f}'.format(subtotal))
        
        print("calculating downpayment")
        dnpymt = new_rvn.calc_downpayment()
        print('${:,.2f}'.format(dnpymt))

        # (4) add new transactions to list of transactions for reservation

        # adding any new transactions to reservation object
        # there are downpayments for equipment
        new_trns_ID = objrepo.next_transaction_ID()
        if dnpymt > 0:
            tdy = booking_date_datetime.day
            new_trns = Transaction(new_trns_ID,new_rvn.resv_id,r"50% down payment",tdy,dnpymt,"CREDIT")
            print("adding downpayment to the reservation's list of transactions...")
            new_rvn.add_transaction(new_trns)

        # assert new_rvn.hasDwnP() == False

        # (5) save changes (newly created reservation)
        if save:
            print("saving changes...")
            objrepo.save_new_reservation(new_rvn)
