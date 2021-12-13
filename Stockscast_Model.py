import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
import random
import math
from datetime import date

#forecast length
n_days = 365
# set seed for Reproducibility
random.seed(10)

# call data from Yahoo Finance
# data=yf.download('QCOM', start='2000-1-2')
# data=yf.download('INTC', start='2000-1-2')
# data=yf.download('NYA', start='2000-1-2')
# data=yf.download('^DJI', start='2000-1-2')
# data=yf.download('JPM', start='2015-1-2')
# data=yf.download('F',start='2018-1-2')
# data=yf.download('GOOGL',start='2000-1-2')
# data=yf.download('BA', start='2015-1-2')
# data=yf.download('KHC')
# data=yf.download('AAPL', start='2015-1-2')
# data=yf.download('FB',start='2000-1-2')
# data=yf.download('NFLX',start='2018-1-2')
# data=yf.download('^IXIC', start='2015-1-2')
# data=yf.download('COST',start='2018-1-2')
# data=yf.download('UBER')
# data=yf.download('MSFT', start='2015-1-2')
# data=yf.download('AMZN', start='2018-10-1')

# data=yf.download('ZM') lags=300
# data=yf.download('TSLA') lags=580, len(array)-1500
# data=yf.download('NVDA', start='2000-1-2')
# data=yf.download('AMD', start='2000-1-2')

#data restructure
data.reset_index(inplace=True,drop=False)
plt.plot(data['Adj Close'])
data['Stock_return'] = data['Close'].pct_change()
data = data.dropna()
df = data[['Stock_return','Date']]
# plt.plot(df['Stock_return'])
df_train = df
array = df_train['Stock_return'].to_numpy()
len(array)
# print(array)
# # plt.plot(array)

# model training
lags = int(len(array) * 0.3)
model = AutoReg(array, lags=lags)
model_fit = model.fit()
yhat = model_fit.predict(len(array)-n_days, len(array))
array = np.append(array,yhat)

# #plotting results
plt.plot(array)
len(array)

# plt.plot(array)
final = (array + 1).cumprod()

plt.figure(figsize=(200, 180))
plt.plot(final[:len(final)])
plt.plot(final[0:len(final)-n_days])


# # #getting data for database
# # raw_forecast = yhat

# # num_final = final[0]
# # num_initial = data['Close'].iloc[0]
# # constant = (num_initial/num_final)

# # preds = raw_forecast * constant
# # preds = [round(num, 2) for num in preds]

# # maximum = preds.index(np.max(preds))
# # minimum = preds.index(np.min(preds))

# # today = date.today()
# # current_date = today.strftime("%Y-%m-%d")
# # current = yf.download('AAPL', start='2021-12-3')
# # current = current['Close'].values.tolist()
# # current = current[0]
# # current = math.ceil(current * 100) / 100



