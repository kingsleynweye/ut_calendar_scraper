# UT Calendar Scraper
## Description
Web scrape semester name, start and end dates from [UT Registrar calendars](https://registrar.utexas.edu/calendars). Also labels observed university and United States holidays.

## Installation
Recommended installation is to install from GitHub using `pip` Version Control System installation within a virtual environment.
Follow these steps to create and activate a virtual environment, and install this package:
```
python -m venv env
source env/bin/activate
python -m pip install git+https://github.com/kingsleynweye/ut_calendar_scraper.git
```

## Usage
See the Command Line Interface help for instructions:
```
python -m ut_calendar_scraper -h
```

The quickest way to get labeled dates within a date range is to make use of the `label_dates()` function in the `Calendar` class
```python
from ut_calendar_scraper.calendar import Calendar

calendar = Calendar(
    start_year=2019,
    start_month=1,
    start_day=1,
    end_year=2019,
    end_month=12, 
    end_day=31
)

result = calendar.label_dates()
```

The result is a `pd.dataFrame` with `date`, `day_of_week`, `day_name`, `is_weekend`, `is_holiday`, `holiday_name`, `is_semester` and `semester_name` columns.