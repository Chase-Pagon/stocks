# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pandas as pd

# Import smtplib (to allow us to email)
import smtplib

curr_year = 2021
before_year = 2019

start_url = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=02%2F08%2F' + str(before_year) + '+-+02%2F08%2F' + str(curr_year) + '&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=5000&page=1'

response = requests.get(start_url)
soup = BeautifulSoup(response.text, "lxml")
table_rows = soup.find_all('tr')
header = table_rows[33].find_all('th')
header_row = [t.text.replace(u'\xa0', u' ').replace(u'\u0394', u'') for t in header]
header_row = header_row[0:len(header_row)-4]
insider_trading_table_buy = [header_row]


for year in range(0, 1):
    url = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=-1&fdr=02%2F08%2F' + str(before_year) + '+-+02%2F08%2F' + str(curr_year) + '&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=5000&page='
    print('Starting ' + str(before_year) + '-' + str(curr_year))
    for i in range(1, 10):
        curr_url = url + str(i)
        response = requests.get(curr_url)
        soup = BeautifulSoup(response.text, "lxml")
        table_rows = soup.find_all('tr')
        time.sleep(1)

        for tr in table_rows[34:]:
            td = tr.find_all('td')
            row = [t.text for t in td]
            insider_trading_table_buy.append(row)
        print('Finished page #' + str(i))

    print('Finished ' + str(before_year) + '-' + str(curr_year))
    curr_year -= 2
    before_year -= 2

df = pd.DataFrame(insider_trading_table_buy)
df.columns = df.iloc[0]
df = df[1:]
df.to_csv('open_insider_trading_table_' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_buy.csv')
