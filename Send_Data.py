import yfinance as yf
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
import random
import math
from datetime import date
from datetime import datetime, timedelta
import json
from numpy import array
import requests
import dateutil.parser as dp
import matplotlib.pyplot as plt
from random import randint
import pandas as pd

# which folder to send forecast data
folder_path = r"C:\Users\aryav\Desktop\Github\Stockscast Model\1 year forecast examples/"

#forecast length
n_days = 260 - 1

# set seed for Reproducibility
random.seed(10)

stock_list = []
stock_name_list = []

# call data from Yahoo Finance
Qualcomm=yf.download('QCOM', start='2000-1-2', actions=False)
Intel=yf.download('INTC', start='2000-1-2', actions=False)
NYSE=yf.download('NYA', start='2000-1-2', actions=False)
DowJones=yf.download('^DJI', start='2000-1-2', actions=False)
JPMorgan=yf.download('JPM', start='2015-1-2', actions=False)
Ford=yf.download('F',start='2018-1-2', actions=False)
Google=yf.download('GOOGL',start='2000-1-2', actions=False)
Boeing=yf.download('BA', start='2015-1-2', actions=False)
Heinz=yf.download('KHC', actions=False)
Apple=yf.download('AAPL', start='2015-1-2', actions=False)
Meta=yf.download('FB',start='2000-1-2', actions=False)
Netflix=yf.download('NFLX',start='2018-1-2', actions=False)
Nasdaq=yf.download('^IXIC', start='2015-1-2', actions=False)
Costco=yf.download('COST',start='2018-1-2', actions=False)
Uber=yf.download('UBER', actions=False)
Microsoft=yf.download('MSFT', start='2015-1-2', actions=False)
Amazon=yf.download('AMZN', start='2018-10-1', actions=False)
Zoom=yf.download('ZM', actions=False)
Tesla=yf.download('TSLA', actions=False)

stock_list.extend((Qualcomm,Intel,NYSE,DowJones,JPMorgan,Ford,Google,Boeing,Heinz,Meta,Netflix,Nasdaq,Costco,Uber,Microsoft,Amazon))
stock_name_list.extend(('qualcomm','intel','nyse','dowjones','JPMorgan','ford','google','boeing','heinz','meta','netflix','nasdaq','costco','uber','microsoft','amazon'))

stocks = {}
news = []

def train_send(stock_name, data, n_lags, x):
    
    data.reset_index(inplace=True,drop=False)
    data['Stock_return'] = data['Close'].pct_change()
    data = data.dropna()
    df = data[['Stock_return','Date']]
    df_train = df
        
    array = df_train['Stock_return'].to_numpy()
    
    if n_lags > -1:
        lags = n_lags
    else:
        lags = int(len(array) * 0.3)
    
    model = AutoReg(array, lags=lags)
    model_fit = model.fit()
    raw_forecast = model_fit.predict(len(array)-n_days-x, len(array)-x)
    array = np.append(array,raw_forecast)
    
    final = (array + 1).cumprod()
    final_preds = final[-260:]
    num_final = final[0]
    num_initial = data['Close'].iloc[0]
    constant = (num_initial/num_final)
    
    preds = final_preds * constant
    preds = [round(num, 2) for num in preds]
    maximum = preds.index(np.max(preds))
    minimum = preds.index(np.min(preds))
   
    startdate = datetime.today()
    enddate = startdate + timedelta(365)
    bs_days=pd.bdate_range(start=startdate, end=enddate)
    unix = bs_days.astype(np.int64) // 10**9
    unix_time = list(unix)

    
    stock_dictionary = {
              "dates": unix_time,
              "preds": preds,
              "max": maximum,
              "min": minimum,
        }
    
    print(len(preds))
    print(len(unix_time))
    
    # stocks[stock_name] = stock_dictionary
    # print(len(preds))
    # fig=plt.figure()
    # plt.figure(figsize=(40, 30))
    # plt.plot(final[:len(final)])
    # plt.plot(final[0:len(final)-260])
    # plt.savefig(folder_path + stock_name) #save as png

# for x in range(len(stock_list)):
#     train_send(stock_name_list[x],stock_list[x], -1, 0)

train_send("zoom",Zoom, 300, 0)

#will add more
# train_send("tesla",Tesla, 580, 1500)

key='image_url'

limit = '1000'
date = str(date.today())
api_url = f'https://api.polygon.io/v2/reference/news?published_utc={date}&limit={limit}&apiKey=BpYLj3XDxfQZfCGlB3OiySFQTzWPBIvK'
data = requests.get(api_url).json()
amount = len(data['results'])

key='image_url'
z=0
q=0

while z <= amount:
    
    x=randint(0,50)

    if ((key in data['results'][x]) and (data['results'][x]['publisher']['name'] != 'Zacks Investment Research')):
              
       id = data['results'][x]['id']
       url = data['results'][x]['article_url']
       title = data['results'][x]['title']
       publisher = data['results'][x]['publisher']['name']
       thumbnail = data['results'][x]['image_url']
       if 'keywords' in data['results'][x]:
          keywords = data['results'][x]['keywords']
       else:
         keywords = []
       api_publish = data['results'][x]['published_utc']
       parsed_api_publish = dp.parse(api_publish)
       parsed_api_publish_in_seconds = parsed_api_publish.timestamp()
       parsed_api_publish_in_seconds=int(parsed_api_publish_in_seconds)
       ticker = data['results'][x]['tickers']
       tickers = [i for n, i in enumerate(ticker) if i not in ticker[:n]]
       locals()["news" + str(q)] = {
                                  "id": id,
                                  "url": url,
                                  "title": title,
                                  "publisher": publisher,
                                  "publishDate": parsed_api_publish_in_seconds,
                                  "thumbnail": thumbnail,
                                  "keywords": keywords,
                                  "tickers": tickers
                                  }
       z=z+1
       q=q+1
    else:
        z=z+1

for i in range(25):
    news.append(locals()["news" + str(i)]) 

dataAryan = {
    "stocks": stocks,
    "news": news,
    "pass": "dev-RZZjmCxk9tTuAHnZ"
}


dataAryanJson = json.dumps(dataAryan)
url = 'https://api.mittaldev.com/stocks-dev/updateStocks'

post = requests.post(url, dataAryanJson)
print(post)







