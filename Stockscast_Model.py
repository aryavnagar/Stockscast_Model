import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
import math
import random
from datetime import date

#forecast length
n_days = 365

# set seed for Reproducibility
random.seed(10)

# call data from Yahoo Finance


# data=yf.download('UBER') lags=250, len(array)-300
# data=yf.download('ZM') lags = 300, len(areray)-300
# data=yf.download('COST',start='2018-1-2') 600 lags

# data=yf.download('AAPL', start='2018-1-2') lags=380, len(array)-365
# data=yf.download('AMZN', start='2018-1-2') lags=380, len(array)-365
# data=yf.download('KHC') lags=400 ,len(array)-120
# data=yf.download('FB',start='2018-1-2')  lags=380, len(array)-365
# data=yf.download('NFLX', start='2018-1-2')  lags=380, len(array)-365
# data=yf.download('BA', start='2000-1-2') lags=400 ,len(array)-120
# data=yf.download('^IXIC', start='2018-1-2') lags=380, len(array)-365
# data=yf.download('QCOM', start='2000-1-2') lags=400 ,len(array)-120
# data=yf.download('MSFT',start='2018-1-1') lags=380, len(array)-365
# data=yf.download('NVDA', start='2000-1-2') lags=400 ,len(array)-120
# data=yf.download('INTC', start='2018-1-2') lags=380, len(array)-365
# data=yf.download('NYA', start='2018-1-2') lags=380, len(array)-365
# data=yf.download('^DJI', start='2018-1-2') lags=380, len(array)-365
# data=yf.download('JPM', start='2000-1-2') lags=400 ,len(array)-120
# data=yf.download('F',start='2018-1-2') lags=380, len(array)-365
# data=yf.download('GOOGL',start='2018-1-2') lags=380, len(array)-365

#data restructure
data.reset_index(inplace=True,drop=False)
plt.plot(data['Close'])
data['Stock_return'] = data['Close'].pct_change()
data = data.dropna()
df = data[['Stock_return','Date']]
# plt.plot(df['Stock_return'])
df_train = df
array = df_train['Stock_return'].to_numpy()
# plt.plot(array)

#model training
x=0
num = math.floor((len(df_train)/2)-1)
while(x < n_days + 1):
    model = AutoReg(array, lags=400)
    model_fit = model.fit()
    yhat = model_fit.predict(len(array)-120, len(array)-120)
    print(yhat)
    array = np.append(array,yhat)
    print(x)
    array = array[~np.isnan(array)]
    x = x+1


#plotting results
plt.plot(array)

len(array)
plt.plot(array)
final = (array + 1).cumprod()

plt.figure(figsize=(40, 30))
plt.plot(final[:len(final)])
plt.plot(final[0:len(final)-365])


#getting data for database
raw_forecast = (final[-365:])

num_final = final[0]
num_initial = data['Close'].iloc[0]
constant = (num_initial/num_final)

preds = raw_forecast * constant
preds = [round(num, 2) for num in preds]

maximum = preds.index(np.max(preds))
minimum = preds.index(np.min(preds))

today = date.today()
current_date = today.strftime("%Y-%m-%d")
current = yf.download('AAPL', start='2021-12-3')
current = current['Close'].values.tolist()
current = current[0]
current = math.ceil(current * 100) / 100



