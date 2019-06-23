import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import QuantLib as ql
from calendar_ql_supported import SetUpSchedule


class BondDefiner(SetUpSchedule):
    def __init__(self, valuation_date, termination_date, tenor, calendar, business_convention,
                 termination_business_convention, date_generation, end_of_month, convention, annual_ytm_rate, face_value,
                 coupon_rate, frequency, coupon_value=None):
        super().__init__(valuation_date, termination_date, tenor, calendar, business_convention,
                         termination_business_convention, date_generation, end_of_month, convention)

        self._annual_ytm_rate = annual_ytm_rate
        self._coupon_rate = coupon_rate
        self._coupon_value = coupon_value
        self._face_value = face_value
        self._s_frequency = frequency
        self.mf_cupon_value = self.get_coupon_value()
        self.mf_nominal_rate = self.get_nominal_rate()
        self.m_price_from_ytm = self.bond_price_using_ytm()



    def get_nominal_rate(self):
        if self._s_frequency == 'Annual':
            nom_rate = self._annual_ytm_rate
        elif self._s_frequency == 'Semiannual':
            nom_rate = self._annual_ytm_rate / 2
        elif self._s_frequency == 'Quarterly':
            nom_rate = self._annual_ytm_rate / 4
        elif self._s_frequency == 'Monthly':
            nom_rate = self._annual_ytm_rate / 12
        return nom_rate

    def get_coupon_value(self):
        if self._coupon_value != None:
            coupon = self._coupon_value
        else:
            coupon = self._face_value * self._coupon_rate
        return coupon

    def bond_price_using_ytm(self):
        price = []
        numb_of_tenor = len(self.ml_dates)
        for i in range(1, numb_of_tenor - 1):  # is ok
            temp = self._coupon_value / (1 + self.mf_nominal_rate) ** i
            price.append(temp)
        return sum(price) + (self._face_value + self._coupon_value) / (1 + self.mf_nominal_rate) ** (numb_of_tenor - 1)


if __name__ == '__main__':
    bond_obj = BondDefiner(valuation_date='2019-06-20',
                           termination_date='2025-06-20',
                           schedule_freq='Annual',
                           # Daily,Monthly,Quarterly,Annual,Semiannual,Bimonthly,Monthly
                           # without arguments it takes valuation_date and termination_date
                           calendar=ql.Poland(),
                           business_convention=ql.Following,  # TODO Find out what does it mean. It is int =0
                           termination_business_convention=ql.Following,
                           date_generation=ql.DateGeneration.Forward,
                           end_of_month=False,
                           convention='ActualActual',
                           ##################################
                           annual_ytm_rate=0.075,
                           face_value=1000,
                           coupon_rate=0.08,
                           coupon_value=50,
                           frequency='Semiannual')


    print('the end')
