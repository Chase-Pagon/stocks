from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
from sklearn import linear_model
from afterhours.afterhours import AfterHours
import matplotlib.pyplot as plt



stock_data = pd.read_csv("stock_data_normal_min.csv")
stock_data.replace([np.inf, -np.inf], np.nan, inplace=True)
stock_data = stock_data.dropna()
percent_change = stock_data['One Day Percent Change']
highs = stock_data['Highest From One Open']
lows = stock_data['Lowest From One Open']
#percent_change_open_close = stock_data['Five Day Percent Change'].copy()

#for i in percent_change.index:
    #percent_change_open_close[i] = ((percent_change[i] / 100 + 1) / (ah_percent_change[i] / 100 + 1) - 1) * 100
max_square_error = 9223372036854775807
amount = 1.0
amount_fit = 0
amounts = [0]
loss_max = 0
gain_max = 0
loss_fit = 0
gain_fit = 0
for risk in range(1,501):
    print(risk/500.0*100)
    for reward in range (1,501):
        amount = 1.0
        points = []
        for i in percent_change.index:
            if highs[i] > risk/10.0:
                amount *= (100 - risk / 10.0) / 100.0
            elif lows[i]*-1 > reward/10:
                amount *= (100 + reward / 10.0) / 100.0
            else:
                amount *= (100 - percent_change[i]) / 100.0
            if amount <= 0:
                print("Broken")
                amount = 0
                break
            points.append(amount)
        m, b = np.polyfit(np.array(range(len(points))), np.array(points), 1)
        line_fit = b + m * np.array(range(len(points)))
        square_error = np.mean((np.array(points) - line_fit) ** 2)
        if square_error < max_square_error and amount > 50:
            max_square_error = square_error
            loss_fit = risk/10.0
            gain_fit = reward/10.0
            amount_fit = amount
        if amount > max(amounts):
            loss_max = risk/10.0
            gain_max = reward/10.0
        amounts.append(amount)

print(max(amounts))
print(loss_max)
print(gain_max)
print("Fit Calcs")
print(amount_fit)
print(loss_fit)
print(gain_fit)
print(max_square_error)
#plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
