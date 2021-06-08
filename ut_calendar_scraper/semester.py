import datetime
import holidays
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
    
    def add_us_holidays(self,observed_us_holidays):
        us_holidays = holidays.US()
        us_holidays.get(self.get_start_date())
        us_holidays.get(self.get_end_date())
        us_holiday_list = []
        
        for date in us_holidays.keys():
            us_holiday = us_holidays.get(date,None)
            
            if us_holiday and us_holiday in observed_us_holidays:
                year = int(date.year)
                month = int(date.month)
                day = int(date.day)

                if self.date_is_in_semester(year,month,day) and not self.date_is_in_holidays(year,month,day)[0]:
                    holiday = Holiday(us_holidays.get(date),year,month,day,year,month,day)
                    us_holiday_list.append(holiday)
        
        self.set_holidays(self.get_holidays() + us_holiday_list)
        
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