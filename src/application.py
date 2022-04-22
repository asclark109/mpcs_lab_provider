from __future__ import annotations
from typing import Union, Hashable
from datetime import datetime, date, timedelta

from reservation import Resrvtn
from equipment import Eqpment
from transaction import Trnsctn
from repository import ObjRepo

##### domain code (APP) ######

class AppInt():

    def reserve(self,custID: str, rsvType: str, date_rs:str, d_o_w:str, hr_strt:str, mm_strt:str, save: bool = True):

        # (0) confirm reservation is 30 days within today
        print("checking date window for booking reservation...")
        rsv_dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
        tdy = date.today()
        dlta = rsv_dt - tdy
        if dlta.days > 30:
            print("Fail. cant reserve more than 30 days into future.")

        # (0) confirm business is open
        print("checking business hours...")
        if d_o_w.upper() in ["MON","TUES","WED","THRS","FRI"]:
            if int(hr_strt) >= 9 and int(hr_strt) < (12+6):
                pass
            else:
                print("Fail. business not open")
                return
            if int(hr_strt) == 5:
                if int(mm_strt) <= 30:
                    pass
                else:
                    print("Fail. business not open")
                    return

        if d_o_w.upper() in ["SAT"]:
            if int(hr_strt) >= 10 and int(hr_strt) <= (12+4):
                pass
            else:
                print("Fail. business not open")
                return
            if int(hr_strt) == (12+3):
                if int(mm_strt) <= 30:
                    pass
                else:
                    print("Fail. business not open")
                    return           

        if d_o_w.upper() in ["SUN"]:
            print("Fail. business not open")
            return    

        # assert rsvType.upper() in [
        #     "WRKSHOP",
        #     "MICRVAC",
        #     "IRRADTR",
        #     "PLYMEXT",
        #     "HIVELCR",
        #     "LIHRVST"]

        # reserve a WORKSHOP
        if rsvType.upper() == "WRKSHOP":
            print("attempting to book workshop...")
            # attempt to book a workshop appointment

            # (1) find available workshops

            # get workshops
            objrepo = ObjRepo()
            wksp_ls = objrepo.getWkps()

            # for each workshop, get the reservation
            # associated with that workshop at the 
            # to-be-desired reservation time. if 
            # reservation list empty, we found a workshop
            # that is not booked at this time. Else, if
            # we've looked at every workshop, then all
            # workshops are booked.
            fnd_wkp = False
            for wksp in wksp_ls:
                # print(wksp.shop_id)
                wksp_id = wksp.shop_id
                dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
                time = datetime.strptime("{}:{}".format(hr_strt,str(mm_strt).zfill(2)),"%H:%M").time()   
                dt_st = datetime.combine(dt,time)
                dt_en = datetime.combine(dt,time)
                rsvn_ls = objrepo.getRwsp(wksp_id,dt_st,dt_en)
                if len(rsvn_ls) == 0:
                    print("workshop available!: id={}".format(wksp_id))
                    fnd_wkp = True
                    wkshp_b = wksp
                    break
                else:
                    # print(wksp_id)
                    print("workshop already booked!: id={}".format(wksp_id))

            if not fnd_wkp:
                print("Fail. did not find available workshop at this time.")
                return

            # (2) create workshop reservation

            # create reservation for this time for this workshop
            print("creating reservation...")
            newID = objrepo.nextRID()
            tdy = date.today().strftime("%m/%d/%Y")
            new_rvn = Resrvtn(newID,custID,tdy,date_rs,d_o_w,hr_strt,mm_strt)
            new_rvn.add_wrk(wkshp_b)
            print("created reservation: {}".format(new_rvn))

            # (3) calculate reservation costs, downpayment

            # calc tot cost
            print("calculating total cost")
            tot_cst = new_rvn.calcCst()
            print('${:,.2f}'.format(tot_cst))

            print("calculating discount")
            discnt = new_rvn.calcDis(tdy,date_rs,tot_cst)
            print('${:,.2f}'.format(discnt))

            subtotl = tot_cst - discnt

            print("calculating downpayment")
            dnpymt = new_rvn.calcDwn(subtotl)
            print('${:,.2f}'.format(dnpymt))

            # (4) add transactions to list of transactions for reservation 

            # adding any new transactions to reservation
            # for now, only downpayment, if present
            # but for reservations there is no downpayment.
            newID = objrepo.nextTID()
            if dnpymt > 0:
                new_tn = Trnsctn(newID,new_rvn.resv_id,r"50% down payment",tdy,'{:.2f}'.format(dnpymt),"CREDIT")
                print("adding downpayment to the reservation's list of transactions...")
                new_rvn.add_trn(new_tn)

            # assert new_rvn.hasDwnP() == False

            # (5) save changes (newly created reservation)
            if save:
                print("saving changes...")
                objrepo.saveRnw(new_rvn)
        
        # handle booking a reservation for piece of equipment
        elif rsvType.upper() in ["MICRVAC", "IRRADTR", "PLYMEXT", "HIVELCR", "LIHRVST"]:

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
            eq_ls = objrepo.getEqTp(rsvType)

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
            eqpmnt: Eqpment
            for eqpmnt in eq_ls:
                eq_id = eqpmnt.eq_id
                # if handling high velocity crusher, we need to confirm there is no
                # additional high velocity crusher reservation 6 hours prior to 
                # desired reservation time, and we need to look 6 hours and 30 minutes
                # past desired reservation time to confirm there is not an existing
                # high velocity crusher reservation. this ensurees there is enough 
                # buffer time for recalibration.
                if rsvType.upper() == "HIVELCR":
                    # left bounded time
                    dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
                    time = datetime.strptime("{}:{}".format(int(hr_strt),str(mm_strt).zfill(2)),"%H:%M").time()   
                    dt_st = datetime.combine(dt,time)
                    # decrement by 5 hours 59 minutes
                    dt_st_B = dt_st - timedelta(hours=5,minutes=59)

                    # right bounded time
                    # if mm_strt == 0:
                    #     hr_end = int(hr_strt) + 6
                    #     mm_end = 30
                    # else:
                    #     hr_end = int(hr_strt) + 6 + 1
                    #     mm_end = 0
                    # time = datetime.strptime("{}:{}".format(hr_end,str(mm_end).zfill(2)),"%H:%M").time()   
                    dt_en = dt_st
                    # increment by 6 hours 29 minutes
                    dt_en_B = dt_en + timedelta(hours=6,minutes=29)
                    print(dt_st_B,dt_en_B)
                else:
                    dt = datetime.strptime(date_rs,'%m/%d/%Y').date()
                    time = datetime.strptime("{}:{}".format(hr_strt,str(mm_strt).zfill(2)),"%H:%M").time()   
                    dt_st_B = datetime.combine(dt,time)
                    dt_en_B = datetime.combine(dt,time)

                rsvn_ls = objrepo.getReqp(eq_id,dt_st_B,dt_en_B)

                if len(rsvn_ls) == 0:
                    print("{} available!: id={}".format(eqpmnt.eq_name,eq_id))
                    fnd_eqt = True
                    eqmnt_b = eqpmnt
                    break
                else:
                    # print(wksp_id)
                    print("{} booked!: id={}".format(eqpmnt.eq_name,eq_id))

            if not fnd_eqt:
                print("Fail. did not find available {} at this time.".format(eq_nms[rsvType.upper()]))
                return

            # (2) create piece of equipment reservation

            # create reservation for this time for this piece of equipment
            print("creating reservation...")
            newID = objrepo.nextRID()
            tdy = date.today().strftime("%m/%d/%Y")
            new_rvn = Resrvtn(newID,custID,tdy,date_rs,d_o_w,hr_strt,mm_strt)
            new_rvn.add_eqp(eqmnt_b)
            print("created reservation: {}".format(new_rvn))

            # (3) calculate total costs, downpayment

            # calc tot cost
            print("calculating total cost")
            tot_cst = new_rvn.calcCst()
            print('${:,.2f}'.format(tot_cst))

            # calc discount
            print("calculating discount")
            discnt = new_rvn.calcDis(tdy,date_rs,tot_cst)
            print('${:,.2f}'.format(discnt))

            # apply discount
            subtotl = tot_cst - discnt

            # calc down payment
            print("calculating downpayment")
            dnpymt = new_rvn.calcDwn(subtotl)
            print('${:,.2f}'.format(dnpymt))

            # (4) add new transactions to list of transactions for reservation

            # adding any new transactions to reservation object
            # there are downpayments for equipment
            newID = objrepo.nextTID()
            if dnpymt > 0:
                new_tn = Trnsctn(newID,new_rvn.resv_id,r"50% down payment",tdy,dnpymt,"CREDIT")
                print("adding downpayment to the reservation's list of transactions...")
                new_rvn.add_trn(new_tn)

            # assert new_rvn.hasDwnP() == True

            # (5) save changes (newly created reservation)
            if save:
                print("saving changes...")
                objrepo.saveRnw(new_rvn)
            
    def cancel(self,custID: str, rsrvID: str, save: bool = True):
        """assumes reservation is not already canceled"""

        print("\ncancelling reservation id={} for customer id={}.".format(rsrvID,custID))
        repo = ObjRepo()
        rsvn = repo.getRsvn(rsrvID)

        # (0) calculate refund
        subtotl = rsvn.calcCst()
        print("subtotal: ",subtotl)
        dwnpay = rsvn.calcDwn(subtotl)
        print("downpayment (50pcnt subtotal): ",dwnpay)
        refund = rsvn.calcRef(rsvn.date_rs,dwnpay)
        print("refund: ",refund)

        # (1) cancel officially
        rsvn.canceld = True

        if refund != 0:
            new_TID = repo.nextTID()
            today = date.today()
            trnsctn = Trnsctn(new_TID, rsrvID, "refund (cancellation)",today,refund,"DEBIT")
            print("adding refund to list of transactions...")
            rsvn.add_trn(trnsctn)

        # save reservation (write new line to text file) and 
        # save new transaction (down payment, if present, to text file)
        if save:
            print("saving changes...")
            repo.saveRCl(rsvn)        

    def viewRep(self,dt_strt: str, dt_end: str):
        print("\nviewing report: reservations by date.")
        repo = ObjRepo()
        rvns_list = repo.getRvns(dt_strt,dt_end)

        headers = ["resv id","date booked", "date resrvd", "start", "end", "customer id", "equipment id","name", "workshop id", "name", "status"]
        header_str = "   ".join(headers)
        to_print = []
        to_print.append(headers)

        headers = ["------","-----------", "-----------", "------","---", "-----------", "------------","----", "-----------", "----", "------"]
        header_str = "   ".join(headers)
        to_print.append(headers)

        for rvn in rvns_list:
            resv_id = rvn.resv_id
            date_bk = rvn.date_bk # mm/dd/yyyy as str
            date_rs = rvn.date_rs # mm/dd/yyyy as str
            custID = rvn.custID
            eqmntID = rvn.eqmnt.eq_id if rvn.eqmnt is not None else "-"
            eqmntNM = rvn.eqmnt.eq_name if rvn.eqmnt is not None else "-"
            wkshpID = rvn.wrkshop.shop_id if rvn.wrkshop is not None else "-"
            wkshpNM = rvn.wrkshop.name if rvn.wrkshop is not None else "-"
            canceld = "CANCELED" if rvn.canceld else "ACTIVE"

            hr_strt = rvn.hr_strt
            mm_strt = rvn.mm_strt

            if mm_strt == 30:
                hr_end = 1 + hr_strt
            else:
                hr_end = hr_strt

            if mm_strt == 0:
                mm_end = 30
            else:
                mm_end = 0

            # print(hr_strt,mm_strt,hr_end,mm_end)

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

            # print( time_st, time_en)

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
        
    def viewTns(self,dt_strt: str, dt_end: str):
        print("\nviewing transactions: transactions by date.")
        repo = ObjRepo()
        trns_list = repo.getTrns(dt_strt,dt_end)

        headers = ["date", "transaction id","resv id", "type", "desc", "amount"]
        header_str = "   ".join(headers)
        to_print = []
        to_print.append(headers)

        headers = ["----", "--------------","-------", "----", "----", "------"]
        header_str = "   ".join(headers)
        to_print.append(headers)

        trnsctn: Trnsctn
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

    def viewRsv(self,custID: str, dt_strt: str, dt_end: str):
        print("\nviewing reservations: reservations by date, customer ID.")
        repo = ObjRepo()
        rvns_list = repo.getRvnC(custID,dt_strt,dt_end)

        headers = ["resv id","date booked", "date resrvd", "start", "end", "customer id", "equipment id","name", "workshop id", "name", "status"]
        header_str = "   ".join(headers)
        to_print = []
        to_print.append(headers)

        headers = ["-------","-----------", "-----------", "------","---", "-----------", "------------","----", "-----------", "----", "------"]
        header_str = "   ".join(headers)
        to_print.append(headers)
        

        for rvn in rvns_list:
            resv_id = rvn.resv_id
            date_bk = rvn.date_bk # mm/dd/yyyy as str
            date_rs = rvn.date_rs # mm/dd/yyyy as str
            custID = rvn.custID
            eqmntID = rvn.eqmnt.eq_id if rvn.eqmnt is not None else "-"
            eqmntNM = rvn.eqmnt.eq_name if rvn.eqmnt is not None else "-"
            wkshpID = rvn.wrkshop.shop_id if rvn.wrkshop is not None else "-"
            wkshpNM = rvn.wrkshop.name if rvn.wrkshop is not None else "-"
            canceld = "CANCELED" if rvn.canceld else "ACTIVE"

            hr_strt = rvn.hr_strt
            mm_strt = rvn.mm_strt

            if mm_strt == 30:
                hr_end = 1 + hr_strt
            else:
                hr_end = hr_strt

            if mm_strt == 0:
                mm_end = 30
            else:
                mm_end = 0

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
