"""commandline program for interacting with program"""

# import modules
import argparse, datetime

# local imports
from application import AppInt

def main():

    # get -h argument by default
    parser = argparse.ArgumentParser()

    # add optional arguments    
    parser.add_argument("-reserve", required=False, nargs=5, metavar=('CST_ID', 'RES_TYPE', 'DATE', 'HH:MM','DURATION_HH'), help="books a reservation for customer CST_ID of type RESRVE_TYPE, one of [WRKSHOP,MICRVAC,IRRADTR,PLYMEXT,HIVELCR,LIHRVST]")
    parser.add_argument("-cancel", required=False,  nargs=2, metavar=('CST_ID', 'RES_ID'),  help="cancels a reservation with id RES_ID for customer CST_ID")
    parser.add_argument("-report", required=False,  action='store_true', help="displays reservations for date range, see -dateL and -dateR")
    parser.add_argument("-transactions", required=False, action='store_true', help="displays transactions for date range, see -dateL and -dateR")
    parser.add_argument("-reservations", required=False, nargs="?",metavar=('CST_ID'),  const="ALL", help="displays reservations for a customer for date range")
    parser.add_argument("-save",  action='store_true', required=False, help="officially saves the changes that would be made from call")

    parser.add_argument("-dateL", required=False, help="date, left bound (for bounding report,transactions,reservations)")
    parser.add_argument("-dateR", required=False, help="date, right bound (for bounding report,transactions,reservations)")

    # Parse the argument
    args = parser.parse_args()

    # fire up app
    app = AppInt()

    # handle optional flags for dateL, dateR
    if args.dateL:
        date_l = args.dateL
    else:
        date_l = "01/01/1500"

    if args.dateR:
        date_r = args.dateR
    else:
        date_r = "01/01/5000"

    # handle arguments
    if args.reserve:
        # unpack args and compute remaining information
        custID = args.reserve[0]
        resType = args.reserve[1]
        dateStr = args.reserve[2]
        hhmmStr = args.reserve[3]
        duration = float(args.reserve[4])

        reservation_start = datetime.datetime.strptime(hhmmStr, '%H:%M')
        hr_start = reservation_start.hour
        mm_start = reservation_start.minute
        
        if args.save:
            to_save = True
        else:
            to_save = False

        app.reserve(custID,resType,dateStr,hr_start,mm_start,duration,to_save)
    
    # unpack args and compute remaining information
    elif args.cancel:
        custID = args.cancel[0]
        rsrvID = args.cancel[1]
        if args.save:
            to_save = True
        else:
            to_save = False
        app.cancel(custID,rsrvID,to_save)

    # unpack args and compute remaining information
    elif args.report:
        app.view_report(dt_strt=date_l,dt_end=date_r)
    
    # unpack args and compute remaining information
    elif args.transactions:
        app.view_transactions(dt_strt=date_l,dt_end=date_r)

    # unpack args and compute remaining information
    elif args.reservations:
        if args.reservations == "ALL":
            app.view_report(dt_strt=date_l,dt_end=date_r)
        else:
            custID = args.reservations[0]
            app.view_reservations(custID=custID,dt_strt=date_l,dt_end=date_r)

        # custID = args.reservations[0]
        # app.viewRsv(custID=,dt_strt=date_l,dt_end=date_r)
    else:
        print("did not understand input.")

if __name__ == "__main__":
    main()