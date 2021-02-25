# imports
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
from datetime import datetime
from datetime import timedelta
yf.pdr_override()

#get stock tickers
url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
df=pd.read_csv(url, sep="|")
symbols = df['Symbol']
#symbols = symbols[0:10]

stock_percent_changes = pd.DataFrame()
stock_highs = pd.DataFrame()
stock_lows = pd.DataFrame()
stock_close_to_open = pd.DataFrame()
stock_open_to_close = pd.DataFrame()
stock_close = pd.DataFrame()
stock_volume = pd.DataFrame()
stock_open = pd.DataFrame()
#getting all stock price changes
c=0
for symbol in symbols:
    c+=1
    print(float(c)*100/symbols.size)
    try:
        stock = pdr.get_data_yahoo(symbol, period='5y')
        stock_percent_changes[symbol] = ((stock['Close'] / stock['Close'].shift())-1)*100
        stock_highs[symbol] = stock['High']
        stock_close[symbol] = stock['Close']
        stock_open[symbol] = stock['Open']
        stock_volume[symbol] = (stock['Volume'] / stock['Volume'].shift()-1)*100
        stock_close_to_open[symbol] = ((stock['Open'] / stock['Close'].shift())-1)*100
        stock_open_to_close[symbol] = ((stock['Close'] / stock['Open'])-1)*100
        stock_lows[symbol] = stock['Low']
        splits = yf.Ticker(symbol).get_splits()
        for time in splits.index:
            stock_percent_changes[symbol][time] = 0
    except:
        print("Bad data")
symbol_to_price_change = pd.DataFrame()
symbol_to_price_change['Symbol'] = stock_percent_changes.idxmin(axis=1)
symbol_to_price_change['Volume Change'] = symbol_to_price_change['Symbol'].copy()
symbol_to_price_change['Prev Day Percent Change'] = symbol_to_price_change['Symbol'].copy()
symbol_to_price_change['Prev Day Afterhours Percent Change'] = symbol_to_price_change['Symbol'].copy()
symbol_to_price_change['Percent Change'] = stock_percent_changes.min(axis=1)
symbol_to_price_change['Afterhours Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['One Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Two Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Three Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Four Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Five Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Six Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Seven Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Eight Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Nine Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Ten Day Percent Change'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From One Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Two Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Three Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Four Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Five Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Six Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Seven Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Eight Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Nine Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Highest From Ten Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From One Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Two Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Three Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Four Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Five Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Six Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Seven Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Eight Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Nine Open'] = symbol_to_price_change['Percent Change'].copy()
symbol_to_price_change['Lowest From Ten Open'] = symbol_to_price_change['Percent Change'].copy()
dates = stock_percent_changes[symbol_to_price_change['Symbol'][symbol_to_price_change['Symbol'].size-1]].index
for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Volume Change'][i] = stock_volume[symbol_to_price_change['Symbol'][i]].loc[dates[i]]
    except:
        symbol_to_price_change['Volume Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['One Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+1] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['One Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Two Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+2] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Two Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Three Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+3] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Three Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Four Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+4] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Four Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Five Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+5] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Five Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Six Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+6] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Six Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Seven Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+7] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Seven Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Eight Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+8] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Eight Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Nine Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+9] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Nine Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Ten Day Percent Change'][i] = ((stock_close[symbol_to_price_change['Symbol'][i]][i+10] / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Ten Day Percent Change'][i] = None


for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Prev Day Percent Change'][i] = stock_percent_changes[symbol_to_price_change['Symbol'][i]].loc[dates[i - 1]]
    except:
        symbol_to_price_change['Prev Day Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From One Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+2]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From One Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Two Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+3]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Two Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Three Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+4]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Three Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Four Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+5]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Four Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Five Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+6]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Five Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Six Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+7]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Six Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Seven Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+8]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Seven Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Eight Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+9]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Eight Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Nine Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+10]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Nine Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Highest From Ten Open'][i] = ((max(stock_highs[symbol_to_price_change['Symbol'][i]][i+1:i+11]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Highest From Ten Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From One Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+2]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From One Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Two Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+3]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Two Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Three Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+4]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Three Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Four Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+5]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Four Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Five Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+6]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Five Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Six Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+7]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Six Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Seven Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+8]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Seven Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Eight Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+9]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Eight Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Nine Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+10]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Nine Open'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Lowest From Ten Open'][i] = ((min(stock_lows[symbol_to_price_change['Symbol'][i]][i+1:i+11]) / stock_open[symbol_to_price_change['Symbol'][i]][i+1]) - 1) * 100
    except:
        symbol_to_price_change['Lowest From Ten Open'][i] = None


for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Afterhours Percent Change'][i] = stock_close_to_open[symbol_to_price_change['Symbol'][i]].loc[dates[i + 1]]
    except:
        symbol_to_price_change['Afterhours Percent Change'][i] = None

for i in range (symbol_to_price_change['Symbol'].size):
    try:
        symbol_to_price_change['Prev Day Afterhours Percent Change'][i] = stock_close_to_open[symbol_to_price_change['Symbol'][i]].loc[dates[i]]
    except:
        symbol_to_price_change['Prev Day Afterhours Percent Change'][i] = None

symbol_to_price_change.to_csv("stock_data_normal_min.csv")



