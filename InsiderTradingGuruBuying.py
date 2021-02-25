import requests
from bs4 import BeautifulSoup
from pandas_datareader import data as pdr
import pandas as pd
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://www.gurufocus.com/insider/summary'
page = requests.get(url)
driver = webdriver.Chrome('/Users/chasepagon/Downloads/chromedriver')

driver.get(url)
time.sleep(5)

curr_date = datetime.now().date()

for d in range(0, 20):

    next_date = curr_date - timedelta(days=179)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    date_first = driver.find_element_by_xpath('//*[@id="components-root"]/div/div[1]/div[5]/div[2]/div/div[3]/input[1]')
    date_first.send_keys(next_date.strftime('%Y-%m-%d'))
    time.sleep(1)

    date_second = driver.find_element_by_xpath('//*[@id="components-root"]/div/div[1]/div[5]/div[2]/div/div[3]/input[2]')
    date_second.send_keys(curr_date.strftime('%Y-%m-%d'))
    time.sleep(1)

    date_second.send_keys(Keys.ENTER)
    time.sleep(5)

    table_rows = soup.find_all('tr')
    header = table_rows[0].find_all('th')
    header_row = [t.text.strip() for t in header]
    header_row = header_row[0:len(header_row)-1]
    insider_trading_table_buy = [header_row]
    insider_trading_table_sell = [header_row]

    num = driver.find_element_by_xpath('//*[@id="components-root"]/div/div[1]/div[8]/div/ul/li[8]')
    num_tables = int(soup.find_all('li')[-1].get_text())

    for i in range(2, num_tables + 1):
        print((float(i)/num_tables)*100)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        table_rows = soup.find_all('tr')

        for tr in table_rows[2:]:
            td = tr.find_all('td')
            row = [t.text for t in td]
            if any('Buy' in s for s in row):
                insider_trading_table_buy.append(row)
            else:
                insider_trading_table_sell.append(row)

        click_number = i
        if i > 6:
            click_number = 6
        elif i == num_tables - 1:
            click_number = 7
        elif i == num_tables:
            click_number = 7

        element = driver.find_element_by_xpath("//*[@id='components-root']/div/div[1]/div[8]/div/ul/li[" + str(click_number) + "]")
        time.sleep(1)
        element.click()
        time.sleep(5)

    dfs = pd.DataFrame(insider_trading_table_sell)
    dfs.columns = dfs.iloc[0]
    dfs = dfs[1:]
    dfb = pd.DataFrame(insider_trading_table_buy)
    dfb.columns = dfb.iloc[0]
    dfb = dfb[1:]

    dfs.to_csv('guru_insider_trading/insider_trading_table_' + curr_date.strftime('%Y-%m-%d') + '_sell.csv')
    dfb.to_csv('guru_insider_trading/insider_trading_table_' + curr_date.strftime("%Y_%m_%d") + '_buy.csv')
    #_%H_%M_%S

    curr_date = next_date

    print(d)

print('DONE')
