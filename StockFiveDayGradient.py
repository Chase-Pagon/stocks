# imports
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
yf.pdr_override()

#get stock tickers
url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
df=pd.read_csv(url, sep="|")
symbols = df['Symbol']
#symbols = symbols[0:10]

stock_close = pd.DataFrame()
stock_volume = pd.DataFrame()
stock_five_day = pd.DataFrame()
stock_square_error = pd.DataFrame()
stock_next_day = pd.DataFrame()
temp_points = pd.DataFrame()
#getting all stock price changes

def get_mean_square_error(stock, five_day_percent, symbol):
    square_errors = np.array([None, None, None, None, None], dtype=float)
    point = []
    for i in range(5, len(five_day_percent)):
        if 20 < five_day_percent[i] < 40:
            points = stock['Close'][i-5:i+1]
            m, b = np.polyfit(np.array(range(len(points))), np.array(points), 1)
            line_fit = b + m * np.array(range(len(points)))
            square_error = np.mean((np.array(points) - line_fit) ** 2)
            square_errors = np.append(square_errors, square_error)
            point.append(points)
        else:
            square_errors = np.append(square_errors, 9223372036854775807)
            point.append([])
    stock_square_error[symbol] = square_errors
    temp_points[symbol] = point

c=0
for symbol in symbols:
    c+=1
    print(float(c)*100/symbols.size)
    try:
        stock = pdr.get_data_yahoo(symbol, period='1y')
        stock_close[symbol] = stock['Close']
        stock_volume[symbol] = (stock['Volume'] / stock['Volume'].shift()-1)*100
        stock_five_day[symbol] = (stock['Close'] / stock['Close'].shift(5) - 1) * 100
        stock_next_day[symbol] = (stock['Close'] / stock['Close'].shift() - 1) * 100
        get_mean_square_error(stock, stock_five_day[symbol], symbol)
    except:
        print("Bad data")

stock_square_error.index = stock_five_day.index.copy(deep=True)
master_frame = pd.DataFrame()
master_frame['Symbol'] = stock_square_error.idxmin(axis=1)
master_frame['Volume Change'] = master_frame['Symbol'].copy(deep=True)
master_frame['Five Day Percent Change'] = master_frame['Symbol'].copy(deep=True)
master_frame['Square Error'] = master_frame['Symbol'].copy(deep=True)
master_frame['Next Day Percent Change'] = master_frame['Symbol'].copy(deep=True)

for i, s in enumerate(master_frame['Symbol']):
    try:
        master_frame['Volume Change'][i] = stock_volume[s][i]
    except:
        master_frame['Volume Change'][i] = None
    try:
        master_frame['Five Day Percent Change'][i] = stock_five_day[s][i]
    except:
        master_frame['Five Day Percent Change'][i] = None
    try:
        master_frame['Square Error'][i] = stock_square_error[s][i]
    except:
        master_frame['Square Error'][i] = None
    try:
        master_frame['Next Day Percent Change'][i] = stock_next_day[s][i + 1]
    except:
        master_frame['Next Day Percent Change'][i] = None


master_frame.to_csv("stock_data_five_day.csv")



