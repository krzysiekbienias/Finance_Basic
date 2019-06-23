import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import QuantLib as ql



class CalendarBoost(): #laverege from QuantLib
    def __init__(self,valuation_date,maturity_date,convention,expiry_date=None):
        self._valuation_date=valuation_date #year-month-days,4-2-2
        self._expiry_date=expiry_date
        self._maturity_date=maturity_date
        self._convention=convention

    def set_days_convention(self, give_name):
        if (give_name == 'Actual360'):
            day_count = ql.Actual360()
            return day_count
        elif (give_name == 'Actual365'):
            day_count = ql.Actual365Fixed()
            return day_count
        elif (give_name == 'ActualActual'):
            day_count = ql.ActualActual()
            return day_count
        elif (give_name == 'Thity360'):
            day_count = ql.Thirty360()
            return day_count
        elif (give_name == 'Business252'):
            day_count = ql.Business252()
            return day_count


    def convert_string_into_ql_object(self,date):
        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:])
        ql_date=ql.Date(day,month,year)
        return ql_date


    def what_day(self,date):
        ql_date=self.convert_string_into_ql_object(date)
        return ql_date.weekday()

    def year_fraction(self):
        day_count=self.chose_convention()
        part_of_year=day_count.yearFraction(self._valuation_date,self._expiry_date)
        return part_of_year



class SetUpSchedule():
    def __init__(self,valuation_date,termination_date,calendar,business_convention,termination_business_convention,date_generation,end_of_month,convention,schedule_freq):
        self._svaluation_date=valuation_date
        self._stermination_date=termination_date
        self._s_schedule_freq = schedule_freq

        self._ql_calendar=calendar
        self._s_business_convention=business_convention
        self._ql_termination_business_convention=termination_business_convention
        self._ql_date_generation=date_generation
        self._b_end_of_month=end_of_month
        self.s_days_conv=convention
        self.m_ql_valuation_date=self.convert_string_into_ql_object(date=self._svaluation_date)
        self.m_ql_termination_date = self.convert_string_into_ql_object(date=self._stermination_date)
        self.m_day_count=self.set_days_convention(give_name=self.s_days_conv)
        self.mql_period_frequency = self.set_scedule_frequency()
        self.m_schedule=self.get_schedule()
        self.ml_dates=self.get_list_of_dates()
        self.ml_yf=self.consecutive_year_fractions()





    def convert_string_into_ql_object(self,date):
        year=int(date[0:4])
        month=int(date[5:7])
        day=int(date[8:])
        ql_date=ql.Date(day,month,year)
        return ql_date

    def set_days_convention(self,give_name):
        if(give_name=='Actual360'):
            day_count = ql.Actual360()
            return day_count
        elif(give_name=='Actual365'):
            day_count = ql.Actual365Fixed()
            return day_count
        elif(give_name=='ActualActual'):
            day_count = ql.ActualActual()
            return day_count
        elif(give_name=='Thity360'):
            day_count = ql.Thirty360()
            return day_count
        elif (give_name == 'Business252'):
            day_count = ql.Business252()
            return day_count

    def set_scedule_frequency(self):
        if self._s_schedule_freq=="Daily":
            return ql.Period(ql.Daily)
        if self._s_schedule_freq=="Weekly":
            return ql.Period(ql.Weekly)
        if self._s_schedule_freq=="Monthly":
            return ql.Period(ql.Monthly)
        if self._s_schedule_freq=="Quarterly":
            return ql.Period(ql.Quarterly)
        if self._s_schedule_freq=="Semiannual":
            return ql.Period(ql.Semiannual)
        if self._s_schedule_freq=="Annual":
            return ql.Period(ql.Annual)
        if self._s_schedule_freq=="Two Dates":
            return ql.Period()







    def get_schedule(self):
            return ql.Schedule(
                self.m_ql_valuation_date,
                self.m_ql_termination_date,
                self.mql_period_frequency,
                self._ql_calendar,
                self._s_business_convention,
                self._ql_termination_business_convention,
                self._ql_date_generation,
                self._b_end_of_month)

    def get_list_of_dates(self):
        return list(self.m_schedule)

    def consecutive_year_fractions(self):
        day_count=self.m_day_count
        l_yf=[]
        for i in range(1,len(self.ml_dates)):
            temp=day_count.yearFraction(self.ml_dates[i-1],self.ml_dates[i])
            l_yf.append(temp)

        return l_yf

if __name__ == '__main__':
    set_up_schedule=SetUpSchedule(valuation_date='2019-06-20',
                                    termination_date = '2020-06-20',
                                    schedule_freq='Monthly',#Daily,Monthly,Quarterly
                                    calendar = ql.Poland(),
                                    business_convention = ql.Following,#TODO Find out what does it mean. It is int =0
                                    termination_business_convention=ql.Following,
                                    date_generation = ql.DateGeneration.Forward,
                                    end_of_month = False,
                                  convention='ActualActual',
                                  )



    print('the end')
