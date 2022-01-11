import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from ut_calendar_scraper.holiday import Holiday
from ut_calendar_scraper.semester import Semester

class Calendar():
    def __init__(self,start_year,start_month,start_day,end_year,end_month,end_day):
        self.set_start_date(start_year,start_month,start_day)
        self.set_end_date(end_year,end_month,end_day)
        self.__UT_REGISTRAR_URL = 'https://registrar.utexas.edu/calendars/'
        self.__SITE_DATE_FMT = '%Y %B %d'
        
    def get_semesters(self):
        return self.__semesters
    
    def get_start_date(self):
        return self.__start_date
    
    def get_end_date(self):
        return self.__end_date
    
    def set_semesters(self,semesters):
        self.__semesters = semesters
    
    def set_start_date(self,year,month,day):
        self.__start_date = datetime.date(year,month,day)
    
    def set_end_date(self,year,month,day):
        self.__end_date = datetime.date(year,month,day)
        
    def get_semester_dates(self):
        dates = []
        
        for semester in self.get_semesters():
            dates.append((semester.get_start_date(),semester.get_end_date()))
        
        return dates
    
    def date_is_in_semesters(self,year,month,day):
        result = (False, None)

        for semester in self.get_semesters():
            if semester.date_is_in_semester(year,month,day):
                result = (True, semester)
                break
            else:
                continue
        
        return result

    def __date_is_winter_break(self,year,month,day):
        calendar_dirs = self.__get_calendar_dirs(year,year)[0]
        semester_dict = {}
        
        for calendar_dir in calendar_dirs:
            semesters = self.get_long_session_semesters(calendar_dir)
            
            for semester in semesters:
                semester_dict[semester.get_title()] = semester
        
        date = datetime.date(year,month,day)
        result = (False,None)

        semester_end_dates = [
            semester_dict[f'Fall Semester {year-1}'].get_end_date(),
            semester_dict[f'Fall Semester {year}'].get_end_date() if f'Fall Semester {year}' in semester_dict.keys() else None
        ]
        semester_start_dates = [
            semester_dict[f'Spring Semester {year}'].get_start_date(),
            semester_dict[f'Spring Semester {year+1}'].get_start_date() if f'Spring Semester {year+1}' in semester_dict.keys() else None
        ]

        for semester_end_date, semester_start_date in zip(semester_end_dates,semester_start_dates):
            if semester_end_date is not None and semester_start_date is not None and semester_end_date < date < semester_start_date:
                start_date = datetime.datetime(semester_end_date.year,semester_end_date.month,semester_end_date.day) + datetime.timedelta(days=1)
                end_date = datetime.datetime(semester_start_date.year,semester_start_date.month,semester_start_date.day) - datetime.timedelta(days=1)
                result = (True,Holiday(
                    'Winter Break',
                    int(start_date.year),
                    int(start_date.month),
                    int(start_date.day),
                    int(end_date.year),
                    int(end_date.month),
                    int(end_date.day),
                ))
                break
            else:
                continue
        
        return result
    
    def date_is_a_holiday(self,year,month,day):
        date = datetime.date(year,month,day)

        if date >= self.get_start_date() and date <= self.get_end_date():
            result = (True,Holiday('Other',year,month,day,year,month,day))
            
            for i, semester in enumerate(self.get_semesters()):
                if semester.date_is_in_semester(year,month,day):
                    result = semester.date_is_in_holidays(year,month,day)
                    break
                
                else:
                    continue
        
        else:
            raise Exception(f'Date must be within {self.get_start_date()} and {self.get_end_date()}')

        if result[0] and result[1].get_title() == 'Other':
            name = Holiday.get_observed_holiday_name(year,month,day)

            if name:
                result = (True,Holiday(name,year,month,day,year,month,day))

            else:
                winter_break_result = self.__date_is_winter_break(year,month,day)

                if winter_break_result[0]:
                    result = winter_break_result
                else:
                    pass

        return result
        
    def __str__(self):
        string = (
            'start_date: ' + str(self.get_start_date())
            + '\nend_date: ' + str(self.get_end_date())
            + '\nsemesters:'
        )
        
        for semester in self.get_semesters():
            string += '\n\n' + str(semester)
        
        return string
    
    def __get_soup(self,calendar_dir):
        url = self.__UT_REGISTRAR_URL + calendar_dir
        response = requests.get(url)
        soup = BeautifulSoup(response.text.encode('UTF-8'), 'html.parser')
        return soup

    def __get_calendar_dirs(self,start_year,end_year):
        year_list = list(range(start_year - 1,end_year + 2,1))
        long_session_dirs = []
        summer_session_dirs = []
        
        for i in range(len(year_list)-1):
            begin = str(year_list[i])[2:]
            end = str(year_list[i+1])[2:]
            long_session_dirs.append(begin+'-'+end)
            summer_session_dirs.append(end+'summer')
        
        return long_session_dirs, summer_session_dirs[0:-1]

    def validate_dt(self,dt):
        try:
            markup = str(dt)
            soup = BeautifulSoup(markup,features='html.parser')
            
            try:
                strike_tag = soup.strike.extract()
            except:
                pass
            
            dt = soup.dt
            
            try:
                dt = dt.get_text().replace('*NEW*','').replace(' -  ','-').strip()
                soup = BeautifulSoup('<dt>'+dt,features='html.parser')
                dt = soup.dt
            except:
                pass
        
        except:
            pass
        
        return dt
    
    def scrape(self):
        long_session_dirs, summer_session_dirs = self.__get_calendar_dirs(self.get_start_date().year,self.get_end_date().year)
        all_semesters = []
        semesters = []

        for calendar_dir in long_session_dirs:
            all_semesters += self.get_long_session_semesters(calendar_dir)
            
        for calendar_dir in summer_session_dirs:
            all_semesters += self.get_summer_session_semesters(calendar_dir)

        for semester in all_semesters:
            if  self.get_start_date() <= semester.get_start_date() <= self.get_end_date() \
                or self.get_start_date() <= semester.get_end_date() <= self.get_end_date() :
                semesters.append(semester)
            else:
                continue

        self.set_semesters(semesters)

    def label_dates(self):
        self.scrape()
        date_range = pd.date_range(self.get_start_date(),self.get_end_date(),freq='D')
        df = pd.DataFrame({'timestamp':date_range})
        df['holiday'] = df['timestamp'].map(lambda x: self.date_is_a_holiday(x.year,x.month,x.day))
        df['is_holiday'] = df['holiday'].map(lambda x: 1 if x[0] else 0)
        df['holiday_name'] = df['holiday'].map(lambda x: x[1].get_title().lower() if x[0] else None)
        df['semester'] = df['timestamp'].map(lambda x: self.date_is_in_semesters(x.year,x.month,x.day))
        df['is_semester'] = df['semester'].map(lambda x: 1 if x[0] else 0)
        df['semester_name'] = df['semester'].map(lambda x: x[1].get_title().split(' ')[0].lower() if x[0] else None)
        df = df.drop(columns=['holiday','semester'])
        df = df[(df['timestamp'].dt.date >= self.get_start_date()) & (df['timestamp'].dt.date <= self.get_end_date())].copy()
        return df
        
    def get_long_session_semesters(self,calendar_dir):
        semester_list = []
        soup = self.__get_soup(calendar_dir)
        semesters = soup.findAll(['dl'])

        for sem in semesters[1:]:
            title = sem.find_previous('h2').get_text()
            year = title.split(' ')[-1]
            
            holidays = []

            for tag in sem:
                try:
                    tag_text = tag.get_text()
                except:
                    continue

                if 'residence halls open' in tag_text:
                    dt = self.validate_dt(tag.find_previous('dt'))
                    month_day = dt.get_text()
                    date = year + ' ' + month_day
                    date = datetime.datetime.strptime(date,self.__SITE_DATE_FMT)
                    start_year = int(date.year)
                    start_month = int(date.month)
                    start_day = int(date.day)
                
                elif 'residence halls close' in tag_text:
                    dt = self.validate_dt(tag.find_previous('dt'))
                    month_day = dt.get_text()
                    date = year + ' ' + month_day
                    date = datetime.datetime.strptime(date,self.__SITE_DATE_FMT)
                    end_year = int(date.year)
                    end_month = int(date.month)
                    end_day = int(date.day)
                
                elif 'Thanksgiving' in tag_text or 'Spring break' in tag_text:
                    dt = self.validate_dt(tag.find_previous('dt'))
                    month_days = dt.get_text()
                    month = month_days.split(' ')[0]
                    days = month_days.split(' ')[-1]
                    holiday_start_day = days[0:2]
                    holiday_end_day = days[3:]
                    string = year + ' ' + month + ' ' + holiday_start_day
                    holiday_start_date = datetime.datetime.strptime(string,self.__SITE_DATE_FMT)
                    string = year + ' ' + month + ' ' + holiday_end_day
                    holiday_end_date = datetime.datetime.strptime(string,self.__SITE_DATE_FMT)
                    
                    if 'Thanksgiving' in tag_text:
                        holiday = Holiday(
                            'Thanksgiving Break',
                            int(holiday_start_date.year),
                            int(holiday_start_date.month),
                            int(holiday_start_date.day),
                            int(holiday_end_date.year),
                            int(holiday_end_date.month),
                            int(holiday_end_date.day),
                        )
                    
                    else:
                        holiday = Holiday(
                            'Spring Break',
                            int(holiday_start_date.year),
                            int(holiday_start_date.month),
                            int(holiday_start_date.day),
                            int(holiday_end_date.year),
                            int(holiday_end_date.month),
                            int(holiday_end_date.day),
                        )
                    
                    holidays.append(holiday)
                
                else:
                    continue

            semester = Semester(title,start_year,start_month,start_day,end_year,end_month,end_day,holidays=holidays)
            semester.get_observed_holidays()
            semester_list.append(semester)
            
        return semester_list

    def get_summer_session_semesters(self,calendar_dir):
        semester_list = []
        soup = self.__get_soup(calendar_dir)
        divs = soup.find_all('div', attrs={'class': 'field body'})
        semesters = divs[0].findAll('dl')
        
        for sem in semesters:
            title = sem.find_previous('h1').get_text()
            year = title.split(' ')[-1]
            holidays = []

            for tag in sem:
                try:
                    tag_text = tag.get_text()
                except:
                    continue

                if 'residence halls open' in tag_text:
                    
                    month_day = tag.find_previous('dt').get_text()
                    date = year + ' ' + month_day
                    date = datetime.datetime.strptime(date,self.__SITE_DATE_FMT)
                    start_year = int(date.year)
                    start_month = int(date.month)
                    start_day = int(date.day)
                
                elif 'residence halls close' in tag_text:
                    month_day = tag.find_previous('dt').get_text()
                    date = year + ' ' + month_day
                    date = datetime.datetime.strptime(date,self.__SITE_DATE_FMT)
                    end_year = int(date.year)
                    end_month = int(date.month)
                    end_day = int(date.day)
                
                else:
                    pass

            semester = Semester(title,start_year,start_month,start_day,end_year,end_month,end_day,holidays=holidays)
            semester.get_observed_holidays()
            semester_list.append(semester)
        
        return semester_list