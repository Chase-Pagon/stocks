from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

insider_trading_data = pd.read_csv('guru_insider_trading/insider_trading_table_2020_12_27_buy.csv')

price_change = insider_trading_data['\n        Price Change Since Insider Trade (%)\n        ']
price_change = [float(p[0:len(p)-1].replace(',','')) for p in price_change]
insider_trading_data['\n        Price Change Since Insider Trade (%)\n        '] = price_change

insider_trading_data = insider_trading_data[insider_trading_data['\n        Price Change Since Insider Trade (%)\n        '] < 1000]

price_change = insider_trading_data['\n        Price Change Since Insider Trade (%)\n        ']
dates = insider_trading_data['\n        Date\n        ']
ymd = "%Y-%m-%d"
dates = [datetime.strptime(d.strip(), ymd).date() for d in dates]


plt.plot(dates, price_change, 'bo')
plt.show()
