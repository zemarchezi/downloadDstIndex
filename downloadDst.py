#%%
###
## Download Dst data from Kyoto website
## 
##
import requests
import json
import csv
import pandas as pd
import datetime
import matplotlib.pyplot as plt
#%%
NUM_MONTHS = 12
NUM_HOURS = 24
table_start_str = '\nDAY\n'
table_end_str = '\n<!-- vvvvv S yyyymm_part3.html'
website = 'http://wdc.kugi.kyoto-u.ac.jp/'
MIN = -999
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]



def year_url(year):
	if year > 1956 and year <= 2016:
		return 'dst_final'
	elif year <= 2021:
		return 'dst_provisional'
	else:
		return 'dst_realtime'


def download(year, downloadDir):

    dst = {}
    y = year

    print('+--- Year', y)
    dst[y] = {}
    for m in range(1, NUM_MONTHS+1):
        print(m)
        month = "{0:02d}".format(m)
        dataType=year_url(y)
        print(dataType)
        month_url = website + dataType+ '/' + str(y) + month + '/index.html'
        print(month_url)
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
    
        dst[y][m] = table
        print('')

    ldf = pd.DataFrame(columns=['dst'])
    for m in range(1, NUM_MONTHS+1):
        month = "{0:0=2d}".format(m)
        print(m)
        # print(days[m-1])
        for d in range(0, days[m-1]):
            for h in range(0, NUM_HOURS):
                print(d)
                dayHr = datetime.datetime(y,m,d+1) + datetime.timedelta(hours=h+1)
                ldf.loc[dayHr,'dst'] = int(dst[y][m][d][h])

    ldf.to_csv(f'{downloadDir}dstIndex{y}.csv')
    return ldf


#%%
if __name__ == '__main__':
	dst = download(2022, downloadDir='./')
	# json2csv()
# %%
