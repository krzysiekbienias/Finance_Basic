from utils.CalendarManagment.calendar_ql_supported import SetUpSchedule
from apps.base_app import BaseApp
from utils.ExcelUtils.excelUtils import ExcelFilesDetails,CreateDataFrame,OutputInExcel
from utils.quantLibUtil import QuantLibConverter
import QuantLib as ql

import utils.logging_util as l_util
from utils.PlotKit.plotCreator import PlotFinanceGraphs

logger=l_util.get_logger(__name__)

class BondDefiner(SetUpSchedule):
    def __init__(self, valuation_date, termination_date,calendar,convention,schedule_freq, business_convention,
                 termination_business_convention, date_generation, end_of_month, annual_ytm_rate, face_value,
                 coupon_rate, frequency, coupon_values=None):
        super().__init__(valuation_date, termination_date,calendar, business_convention,
                         termination_business_convention, date_generation, end_of_month, convention,schedule_freq)

        self._annual_ytm_rate = annual_ytm_rate
        self._coupon_rate = coupon_rate
        self._coupon_value = coupon_values
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
            temp = self.mf_cupon_value / (1 + self.mf_nominal_rate) ** i
            price.append(temp)
        return sum(price) + (self._face_value + self.mf_cupon_value) / (1 + self.mf_nominal_rate) ** (numb_of_tenor - 1)

class BondsRun(BaseApp):
        def __init__(self, **app_params):
            app_name = 'bond'
            """we populate input from excel"""
            self._tab_name1 = ''
            self._tab_name2 = ''
            self._control_path = ''
            self._file_name = ''
            super().__init__(app_name, app_params)

            #################################----Load Control File----##################################
            self.loadControlFile = CreateDataFrame(file_name=self._file_name, path=self._control_path)
            self.dictionaryOfControlFile = self.loadControlFile.create_data_frame_from_excel()
            #################################----Load Control File----##################################

            self.controlFileBonds=self.dictionaryOfControlFile[self._tab_name1]
            self.qlConverter=QuantLibConverter(calendar=self.controlFileBonds.loc[4,'Value'])


            bond_obj=BondDefiner(valuation_date=self.controlFileBonds.loc[0,'Value'],
                                 termination_date=self.controlFileBonds.loc[1,'Value'],
                                 schedule_freq=self.controlFileBonds.loc[2,'Value'],
                                 calendar=self.qlConverter.mqlCalendar,
                                 convention=self.controlFileBonds.loc[3,'Value'],
                                 end_of_month=self.controlFileBonds.loc[8, 'Value'],
                                 business_convention=self.qlConverter.mqlBusinessConvention,
                                 termination_business_convention=self.qlConverter.mqlTerminationBusinessConvention,
                                 date_generation=ql.DateGeneration.Forward,
                                 annual_ytm_rate=self.controlFileBonds.loc[0,'Bond Value'],
                                 face_value=self.controlFileBonds.loc[1,'Bond Value'],
                                 coupon_rate=self.controlFileBonds.loc[2,'Bond Value'],
                                 coupon_values=self.controlFileBonds.loc[3,'Bond Value'],
                                 frequency=self.controlFileBonds.loc[4,'Bond Value'])

            logger.info('Bond Object has been created')





