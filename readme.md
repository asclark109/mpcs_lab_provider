# Usage

code demonstrated on windows machine at terminal. on linux, python interpretter will be referenced with ```python3```.

## help

Type **```python main.py -h```** for help

```bash
(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -h                      
usage: main.py [-h] [-reserve CST_ID RES_TYPE DATE HH:MM DURATION_HH] [-cancel CST_ID RES_ID] [-report] [-transactions] [-reservations [CST_ID]] [-save] [-dateL DATEL] [-dateR DATER]

optional arguments:
  -h, --help            show this help message and exit
  -reserve CST_ID RES_TYPE DATE HH:MM DURATION_HH
                        books a reservation for customer CST_ID of type RESRVE_TYPE, one of [WRKSHOP,MICRVAC,IRRADTR,PLYMEXT,HIVELCR,LIHRVST]
  -cancel CST_ID RES_ID
                        cancels a reservation with id RES_ID for customer CST_ID
  -report               displays reservations for date range, see -dateL and -dateR
  -transactions         displays transactions for date range, see -dateL and -dateR
  -reservations [CST_ID]
                        displays reservations for a customer for date range
  -save                 officially saves the changes that would be made from call
  -dateL DATEL          date, left bound (for bounding report,transactions,reservations)
  -dateR DATER          date, right bound (for bounding report,transactions,reservations)
```

## View Report

**```python main.py -report [-dateL MM/DD/YYYY] [-dateR MM/DD/YYYY]```** to see reservations.

```[-dateL MM/DD/YYYY] [-dateR MM/DD/YYYY]``` are optional flags to limit output.

Examples:
>python main.py -report\
python main.py -report -dateL 4/2/2022\
python main.py -report -dateR 4/2/2022\
python main.py -report -dateL 4/2/2022 -dateR 4/2/2022\

```bash
(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -report

viewing report: reservations by date.
resv id  date booked  date resrvd  start     end       customer id  equipment id  name                                  workshop id  name        status
-------  -----------  -----------  ------    ---       -----------  ------------  ----                                  -----------  ----        ------
1        03/17/2022   04/02/2022   10:00 am  10:30 am  1            -             -                                     1            workshop 1  ACTIVE
2        03/17/2022   04/02/2022   12:30 am  1:00 pm   6            4             irradiator #2                         -            -           CANCELED
3        03/27/2022   04/02/2022   3:30 pm   4:00 pm   5            1             mini microvac #1                      -            -           ACTIVE
4        03/27/2022   04/02/2022   10:00 am  10:30 am  1            1             mini microvac #1                      -            -           ACTIVE
5        03/27/2022   04/04/2022   10:00 am  10:30 am  3            -             -                                     1            workshop 1  ACTIVE
6        03/28/2022   04/04/2022   12:30 am  1:00 pm   2            -             -                                     1            workshop 1  ACTIVE
7        03/28/2022   04/04/2022   3:30 pm   4:00 pm   1            -             -                                     1            workshop 1  ACTIVE
8        03/28/2022   04/04/2022   10:00 am  10:30 am  1            -             -                                     2            workshop 2  ACTIVE
9        03/28/2022   04/04/2022   10:00 am  10:30 am  3            1             mini microvac #1                      -            -           ACTIVE
10       03/29/2022   04/05/2022   9:00 am   9:30 am   8            -             -                                     1            workshop 1  ACTIVE
11       03/29/2022   04/05/2022   10:30 am  11:00 am  2            9             1.21 gigawatt lightning harvester #1  -            -           ACTIVE
12       03/29/2022   04/05/2022   9:00 am   9:30 am   5            -             -                                     2            workshop 2  ACTIVE
13       03/29/2022   04/05/2022   9:00 am   9:30 am   8            -             -                                     3            workshop 3  ACTIVE
14       03/29/2022   04/05/2022   9:00 am   9:30 am   1            -             -                                     4            workshop 4  ACTIVE
15       03/29/2022   04/06/2022   2:00 pm   2:30 pm   6            -             -                                     1            workshop 1  ACTIVE
16       03/29/2022   04/06/2022   2:30 pm   3:00 pm   5            -             -                                     1            workshop 1  ACTIVE
17       03/29/2022   04/06/2022   2:30 pm   3:00 pm   9            -             -                                     2            workshop 2  CANCELED
18       03/29/2022   04/06/2022   2:00 pm   2:30 pm   1            -             -                                     2            workshop 2  ACTIVE
19       03/29/2022   04/06/2022   2:00 pm   2:30 pm   9            -             -                                     3            workshop 3  CANCELED
20       03/29/2022   04/06/2022   2:00 pm   2:30 pm   7            -             -                                     4            workshop 4  ACTIVE
21       04/06/2022   05/27/2022   1:00 pm   1:30 pm   7            6             polymer extruder #2                   -            -           CANCELED
```

## View Reservations

**```python main.py -reservations CUSTOMER_ID [-dateL MM/DD/YYYY] [-dateR MM/DD/YYYY]```** to see reservations by customer.

```CUSTOMER_ID``` is an integer (e.g. 1,2,3,...). represented as a string unique identifier in code

```[-dateL MM/DD/YYYY] [-dateR MM/DD/YYYY]``` are optional flags to limit output.

Examples:
>python main.py -reservations 1\
python main.py -reservations 1 -dateL 4/2/2022\
python main.py -reservations 1 -dateR 4/2/2022\
python main.py -reservations 1 -dateL 4/2/2022 -dateR 4/2/2022\

```bash
(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -reservations 1 -dateL 4/3/2022

viewing reservations: reservations by date, customer ID.
resv id  date booked  date resrvd  start     end       customer id  equipment id  name  workshop id  name        status
-------  -----------  -----------  ------    ---       -----------  ------------  ----  -----------  ----        ------
7        03/28/2022   04/04/2022   3:30 pm   4:00 pm   1            -             -     1            workshop 1  ACTIVE
8        03/28/2022   04/04/2022   10:00 am  10:30 am  1            -             -     2            workshop 2  ACTIVE
14       03/29/2022   04/05/2022   9:00 am   9:30 am   1            -             -     4            workshop 4  ACTIVE
18       03/29/2022   04/06/2022   2:00 pm   2:30 pm   1            -             -     2            workshop 2  ACTIVE
```

## View Transactions

**```python main.py -tranasactions [-dateL MM/DD/YYYY] [-dateR MM/DD/YYYY]```** to see transactions by date.

```[-dateL MM/DD/YYYY] [-dateR MM/DD/YYYY]``` are optional flags to limit output.

Examples:
>python main.py -transactions\
python main.py -transactions -dateL 3/2/2022\
python main.py -transactions -dateR 3/29/2022\
python main.py -transactions -dateL 3/2/2022 -dateR 3/29/2022\

```bash
(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -transactions -dateR 3/29/2022 

viewing transactions: transactions by date.
date       transaction id  resv id  type    desc                amount
----       --------------  -------  ----    ----                ------
3/17/2022  1               1        CREDIT  '50% down payment'  +$37.13
3/17/2022  2               2        CREDIT  '50% down payment'  +$832.50
3/27/2022  3               3        CREDIT  '50% down payment'  +$375.00
3/27/2022  4               4        CREDIT  '50% down payment'  +$375.00
3/27/2022  5               5        CREDIT  '50% down payment'  +$49.50
3/28/2022  6               6        CREDIT  '50% down payment'  +$49.50
3/28/2022  7               7        CREDIT  '50% down payment'  +$49.50
3/28/2022  8               8        CREDIT  '50% down payment'  +$49.50
3/28/2022  9               9        CREDIT  '50% down payment'  +$500.00
3/29/2022  10              10       CREDIT  '50% down payment'  +$49.50
3/29/2022  11              11       CREDIT  '50% down payment'  +$4,400.00
3/29/2022  12              12       CREDIT  '50% down payment'  +$49.50
3/29/2022  13              13       CREDIT  '50% down payment'  +$49.50
3/29/2022  14              14       CREDIT  '50% down payment'  +$49.50
3/29/2022  15              15       CREDIT  '50% down payment'  +$49.50
3/29/2022  16              16       CREDIT  '50% down payment'  +$49.50
3/29/2022  17              17       CREDIT  '50% down payment'  +$49.50
3/29/2022  18              18       CREDIT  '50% down payment'  +$49.50
3/29/2022  19              19       CREDIT  '50% down payment'  +$49.50
3/29/2022  20              20       CREDIT  '50% down payment'  +$49.50
```

## cancel reservation

To cancel a reservation, the user of the program must know the reservation ID of the reservation they want to cancel. For now I am also requiring customerID be provided, but it is not actually used in the code. 

**```python main.py -cancel CUSTOMER_ID RESERVATION_ID [-save]```** to cancel the reservation.

Adding the ```-save``` flag makes an official cancellation. This allows you to first execute the cancellation to see what would happen, and then you can add the save flag to make it an official change

Examples: cancel reservationID 7, which is also associated with customerID 1.
>python main.py -cancel 1 7

Long example: we look up reservations on customer 1, we identify we want to cancel reservation 7, and we cancel it, and then we look at the reservation again to see it is canceled.

```bash
>(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -reservations 1

viewing reservations: reservations by date, customer ID.
resv id  date booked  date resrvd  start     end       customer id  equipment id  name              workshop id  name        status
-------  -----------  -----------  ------    ---       -----------  ------------  ----              -----------  ----        ------
1        03/17/2022   04/02/2022   10:00 am  10:30 am  1            -             -                 1            workshop 1  ACTIVE
4        03/27/2022   04/02/2022   10:00 am  10:30 am  1            1             mini microvac #1  -            -           ACTIVE
7        03/28/2022   04/04/2022   3:30 pm   4:00 pm   1            -             -                 1            workshop 1  ACTIVE
8        03/28/2022   04/04/2022   10:00 am  10:30 am  1            -             -                 2            workshop 2  ACTIVE
14       03/29/2022   04/05/2022   9:00 am   9:30 am   1            -             -                 4            workshop 4  ACTIVE
18       03/29/2022   04/06/2022   2:00 pm   2:30 pm   1            -             -                 2            workshop 2  ACTIVE

(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -cancel 1 7 -save

cancelling reservation id=7 for customer id=1.
subtotal:  49.5
downpayment (50pcnt subtotal):  0.0
refund:  0
saving changes...

viewing reservations: reservations by date, customer ID.
resv id  date booked  date resrvd  start     end       customer id  equipment id  name              workshop id  name        status
-------  -----------  -----------  ------    ---       -----------  ------------  ----              -----------  ----        ------
1        03/17/2022   04/02/2022   10:00 am  10:30 am  1            -             -                 1            workshop 1  ACTIVE
4        03/27/2022   04/02/2022   10:00 am  10:30 am  1            1             mini microvac #1  -            -           ACTIVE
7        03/28/2022   04/04/2022   3:30 pm   4:00 pm   1            -             -                 1            workshop 1  CANCELED
8        03/28/2022   04/04/2022   10:00 am  10:30 am  1            -             -                 2            workshop 2  ACTIVE
14       03/29/2022   04/05/2022   9:00 am   9:30 am   1            -             -                 4            workshop 4  ACTIVE
18       03/29/2022   04/06/2022   2:00 pm   2:30 pm   1            -             -                 2            workshop 2  ACTIVE
```

## make reservation

To make a reservation, the user of the program must provide: customerID(str), reservation_type(str), date(MM/DD/YYYY), start_time(HH:MM), duration(hours, as a float).

**```python main.py -reserve CUSTOMER_ID RESERVATION_TYPE DATE HH:MM DURATION_HH [-save]```** to make the reservation.

```RESERVATION_TYPE``` is one of ```{WRKSHOP,MICRVAC,IRRADTR,PLYMEXT,HIVELCR,LIHRVST}```.

Adding the ```-save``` flag makes an official reservation, allowing you to probe what would happen before making reservation.

Example: reserve for customerID=3 a workshop on 4/3/2022 at 1:00 pm for 30 minutes
>python main.py -reserve 3 WRKSHOP 4/3/2022 13:00 0.5

Long example: let's keep trying to book an Irradiator on same day, same time until all of them are booked and the machine cannot be reserved.
```bash
(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -reserve 3 IRRADTR 4/2/2022 13:00 0.5 -save
checking date window for booking reservation...
checking business hours...
attempting to book piece of equipment: Irradiator...
irradiator #1 available!: id=3
creating reservation...
created reservation: <reservation: id= 22, date= 2022-04-02 13:00:00, duration(hrs)= 0.5, item= irradiator #1>
calculating total cost
$1,110.00
calculating discount
$0.00
calculating subtotal (total cost - discount)
$1,110.00
calculating downpayment
$555.00
adding downpayment to the reservation's list of transactions...
saving changes...

(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -reserve 3 IRRADTR 4/2/2022 13:00 0.5 -save
checking date window for booking reservation...
checking business hours...
attempting to book piece of equipment: Irradiator...
irradiator #1 booked!: id=3
irradiator #2 available!: id=4
creating reservation...
created reservation: <reservation: id= 23, date= 2022-04-02 13:00:00, duration(hrs)= 0.5, item= irradiator #2>
calculating total cost
$1,110.00
calculating discount
$0.00
calculating subtotal (total cost - discount)
$1,110.00
calculating downpayment
$555.00
adding downpayment to the reservation's list of transactions...
saving changes...

(base) C:\code\51220_applied_soft_eng\mpcs_lab_provider\src>python main.py -reserve 3 IRRADTR 4/2/2022 13:00 0.5 -save
checking date window for booking reservation...
checking business hours...
attempting to book piece of equipment: Irradiator...
irradiator #1 booked!: id=3
irradiator #2 booked!: id=4
Fail. did not find available Irradiator at this time.
```