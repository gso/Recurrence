
from datetime import date
from yearmonth import YearMonth
import recurrence


# Initial tests


# check 31 Jan 1 mnth period returns correct Feb date

rc = recurrence.MonthsBasedRecurrence(anchor=YearMonth(2012, 1), period=1, ordinal=31)
d = rc.get_occurrence(1)
print(d)


# check can now recur on any day in a period,
# though note the algorithm:
# i) does not accommodate a case of e.g. the last 
# day of the 3rd mnth in a 5 mnth period
# ii) does not accommodate a case of e.g. the first
# Mon in the first full week of the month

ym = YearMonth(2012, 1)
rc = recurrence.MonthsBasedRecurrence(ym, 2, -1)
d = rc.get_occurrence(1)
print(d)

ym = YearMonth(2012, 1)
rc = recurrence.MonthsBasedRecurrence(ym, 2, 40)
d = rc.get_occurrence(1)
print(d)

ym = YearMonth(2012, 8)
rc = recurrence.MonthsBasedRecurrence(ym, 1, -1, day=recurrence.MON)
d = rc.get_occurrence(1)
print(d)

ym = YearMonth(2012, 8)
rc = recurrence.MonthsBasedRecurrence(ym, 1, 1, day=recurrence.MON)
d = rc.get_occurrence(1)
print(d)


