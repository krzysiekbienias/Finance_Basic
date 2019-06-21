import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import QuantLib as ql

sys.path.append('../CalendarHandling')
from calendar_kb import ScenariosCalendar

#
# class Rates_Dependency(ScenariosCalendar):
#     def __init__(self,t,expiry_date,maturity_date):
#         self._t=t
#         self._expiry_date=expiry_date
#         self,_maturity_date=maturity_date







class Rates_Converter(CalendarBoost):
    def __init__(self,valuation_date,maturity_date,spot_rate=None,discount_factor=None,expiry_date=None):
        CalendarBoost.__init__(valuation_date,maturity_date,expiry_date=None)
        self._spot_rate=spot_rate
        self._discount_factor=discount_factor
        self._expiry_date=expiry_date


if __name__ == '__main__':
    o_calendarboost=CalendarBoost(valuation_date='2018-08-22',expiry_date='2018-09-22',maturity_date='2018-11-22')
    a=o_calendarboost.convert_string_into_ql_object(date=o_calendarboost._valuation_date)
    b=o_calendarboost.what_day(date=o_calendarboost._valuation_date)
    print("the end")