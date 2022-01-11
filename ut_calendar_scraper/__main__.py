import argparse
import json
import os
import sys
from ut_calendar_scraper.calendar import Calendar

def main():
    parser = argparse.ArgumentParser(prog='ut_calendar_scraper',description='Scrape semester and holiday dates from the UT Registrar\'s website.')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.4')
    parser.add_argument('start_year',type=int,help='Period start year')
    parser.add_argument('start_month',type=int,help='Period start month')
    parser.add_argument('start_day',type=int,help='Period start day')
    parser.add_argument('end_year',type=int,help='Period end year')
    parser.add_argument('end_month',type=int,help='Period end month')
    parser.add_argument('end_day',type=int,help='Period end day')
    parser.add_argument('-f','--filepath',default=None,dest='filepath',type=str,help='Filepath to write to.')
    args = parser.parse_args()

    calendar = Calendar(args.start_year,args.start_month,args.start_day,args.end_year,args.end_month,args.end_day)
    data = calendar.label_dates()

    if args.filepath:
        extension = args.filepath.split('.')[-1]
        directories = '/'.join(args.filepath.split('/')[0:-1])

        if len(directories) > 0:
            os.makedirs(directories,exist_ok=True)
        else:
            pass

        if extension == 'csv':
            data.to_csv(args.filepath,index=False)
        elif extension == 'json':
            data.to_json(args.filepath,indent=4,orient='records')
        else:
            raise Exception(f'Unsupported filetype parsed: .{extension}')
    else:
        print(data.to_json(indent=4,orient='records'))
    
if __name__ == "__main__":
    sys.exit(main())