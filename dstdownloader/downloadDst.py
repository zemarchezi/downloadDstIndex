###
## Download Dst data from Kyoto website
## 
##
import requests
import pandas as pd
import datetime
import calendar



def year_url(year):
    current_year = datetime.datetime.now().year
    if year > 1956 and year < current_year-6:
        return 'dst_final'
    elif year < current_year:
        return 'dst_provisional'
    else:
        return 'dst_realtime'

def downloadDst(year):

    NUM_MONTHS = 12 #months in a year
    NUM_HOURS = 24 # hours in a day
    table_start_str = '\nDAY\n'
    table_end_str = '\n<!-- vvvvv S yyyymm_part3.html'
    website = 'http://wdc.kugi.kyoto-u.ac.jp/'
    MIN = -999 # missing data

    dst = {}
    current_year = datetime.datetime.now().year
    if year == current_year:
        NUM_MONTHS = datetime.datetime.now().month - 1

    print(f'Downloading data of Year {year}')
    dst[year] = {}
    for m in range(1, NUM_MONTHS+1):
        month = f"{m:0=2d}"
        month_url = f"{website}{year_url(year)}/{year}{month}/index.html"
        print(month_url)
        print(f"Retrieving data for {calendar.month_name[m]}, {year}")
        r = requests.get(month_url)
        table_start = r.content.find(table_start_str.encode()) + len(table_start_str)
        table_end = r.content.find(table_end_str.encode())
        table = r.content[table_start: table_end]
        table = table.split(b'\n')
        table = list(filter(None, table))
        # table corresponds to one month of data
        # no. of days * no. of hours
        # list of strings with data
        for day in range(len(table)):
            p = table[day].decode()
            r = p.replace('-',' -').split(' ')
            r = list(filter(None, r))
            r.pop(0) # remove date
            table[day] = [x for x in r]
    
        dst[year][m] = table
        print('')

    dst_df = pd.DataFrame(columns=['dst'])
    for m in range(1, NUM_MONTHS+1):
        month = f"{m:0=2d}"
        # print(days[m-1])
        days_in_month = calendar.monthrange(year,int(month))
        for d in range(0, days_in_month[1]):
            for h in range(0, NUM_HOURS):
                print(d)
                dayHr = datetime.datetime(year,m,d+1) + datetime.timedelta(hours=h+1)
                dst_df.loc[dayHr,'dst'] = int(dst[year][m][d][h])

    dst_df.to_csv(f'dstIndex{year}.csv')
    return dst_df


if __name__ == '__main__':
	pass
    # dst = download(2023)
	

