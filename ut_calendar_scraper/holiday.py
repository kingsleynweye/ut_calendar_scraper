import datetime
import holidays

class Holiday:
    DEFAULT_OBSERVED_HOLIDAYS = (
        'Christmas Day',
        'Christmas Eve',
        'Day After Christmas',
        'Emancipation Day In Texas',
        'Friday After Thanksgiving',
        'Independence Day',
        'Labor Day',
        'Martin Luther King, Jr. Day',
        'Memorial Day'
        'New Year\'s Day',
        'Thanksgiving',
    )

    def __init__(self,title,start_year,start_month,start_day,end_year,end_month,end_day):
        self.set_title(title)
        self.set_start_date(start_year,start_month,start_day)
        self.set_end_date(end_year,end_month,end_day)
        
    def get_title(self):
        return self.__title
    
    def get_start_date(self):
        return self.__start_date
    
    def get_end_date(self):
        return self.__end_date
    
    def set_title(self,title):
        self.__title = title
        
    def set_start_date(self,year,month,day):
        self.__start_date = datetime.date(year,month,day)
    
    def set_end_date(self,year,month,day):
        self.__end_date = datetime.date(year,month,day)
        
    def date_is_in_holiday(self,year,month,day):
        date = datetime.date(year,month,day)
        return date >= self.get_start_date() and date <= self.get_end_date()
    
    def __str__(self):
        return (
            'title: ' + self.get_title()
            + '\nstart_date: ' + str(self.get_start_date())
            + '\nend_date: ' + str(self.get_end_date())
        )

    @staticmethod
    def get_observed_holiday_name(year,month,day,observed_holidays=None):
        name = holidays.CountryHoliday('US',state='TX').get(datetime.date(year,month,day))
        observed_holidays = Holiday.DEFAULT_OBSERVED_HOLIDAYS if observed_holidays is None else observed_holidays

        if name and name.replace('(Observed)','').strip() in observed_holidays:
            return name
        else:
            return None