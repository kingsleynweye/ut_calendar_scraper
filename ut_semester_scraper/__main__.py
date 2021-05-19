import argparse
import inspect
import sys
from ut_semester_scraper.calendar import Calendar

def main():
    parser = argparse.ArgumentParser(prog='ut_semester_scraper',description='Scrape semester and holiday dates from the UT Registrar\'s website.')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('start_year',type=int,help='Period start year')
    parser.add_argument('start_month',type=int,help='Period start month')
    parser.add_argument('start_day',type=int,help='Period start day')
    parser.add_argument('end_year',type=int,help='Period end year')
    parser.add_argument('end_month',type=int,help='Period end month')
    parser.add_argument('end_day',type=int,help='Period end day')
    
    args = parser.parse_args()
    calendar = Calendar(args.start_year,args.start_month,args.start_day,args.end_year,args.end_month,args.end_day)
    # calendar.scrape()
    # print(calendar)
    calendar.label_dates()
    
if __name__ == "__main__":
    sys.exit(main())