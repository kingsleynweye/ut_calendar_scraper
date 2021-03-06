import datetime
import pandas as pd
from ut_calendar_scraper.holiday import Holiday

class Semester:
    def __init__(self,title,start_year,start_month,start_day,end_year,end_month,end_day,holidays=[]):
        self.set_title(title)
        self.set_start_date(start_year,start_month,start_day)
        self.set_end_date(end_year,end_month,end_day)
        self.set_holidays(holidays)
        
    def get_title(self):
        return self.__title
    
    def get_start_date(self):
        return self.__start_date
    
    def get_end_date(self):
        return self.__end_date
    
    def get_holidays(self):
        return self.__holidays
    
    def set_title(self,title):
        self.__title = title
        
    def set_start_date(self,year,month,day):
        self.__start_date = datetime.date(year,month,day)
    
    def set_end_date(self,year,month,day):
        self.__end_date = datetime.date(year,month,day)
        
    def set_holidays(self,holidays):
        self.__holidays = holidays

    def get_observed_holidays(self):
        observed_holiday_list = []
        start_timestamp = datetime.datetime(self.get_start_date().year,self.get_start_date().month,self.get_start_date().day)
        end_timestamp = datetime.datetime(self.get_end_date().year,self.get_end_date().month,self.get_end_date().day)
        timestamps = pd.date_range(start_timestamp,end_timestamp,freq='D')
        
        for timestamp in timestamps:
            year = timestamp.year
            month = timestamp.month
            day = timestamp.day
            name = Holiday.get_observed_holiday_name(year,month,day)

            if name:
                holiday = Holiday(name,year,month,day,year,month,day)
                observed_holiday_list.append(holiday)
            
            else:
                continue
        
        self.set_holidays(self.get_holidays() + observed_holiday_list)
        
    def date_is_in_semester(self,year,month,day):
        date = datetime.date(year,month,day)
        return date >= self.get_start_date() and date <= self.get_end_date()
    
    def date_is_in_holidays(self,year,month,day):
        result = (False, None)

        for holiday in self.get_holidays():
            if holiday.date_is_in_holiday(year,month,day):
                result = (True, holiday)
                break

        return result
            
    def __str__(self):
        string = (
            'title: ' + self.get_title()
            + '\nstart_date: ' + str(self.get_start_date())
            + '\nend_date: ' + str(self.get_end_date())
            + '\nholidays:'
        )
        if self.get_holidays != None:
            for holiday in self.get_holidays():
                string += '\n....' + str(holiday)
        else:
            string += None
        return string