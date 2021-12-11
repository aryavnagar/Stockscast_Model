import yfinance as yf
import numpy as np
from statsmodels.tsa.ar_model import AutoReg
import random
import math
from datetime import date
import json
from numpy import array
import requests
import dateutil.parser as dp
import matplotlib.pyplot as plt
plt.ioff()
from random import randint

# which folder to send forecast data
folder_path = r"C:\Users\aryav\Desktop\Github\Stockscast Model\1 year forecast examples/"

#forecast length
n_days = 365 - 1

# set seed for Reproducibility
random.seed(10)

# call data from Yahoo Finance
Qualcom=yf.download('QCOM', start='2000-1-2', actions=False)
Intel=yf.download('INTC', start='2000-1-2', actions=False)
NYSE=yf.download('NYA', start='2000-1-2', actions=False)
DowJones=yf.download('^DJI', start='2000-1-2', actions=False)
JPMorgan=yf.download('JPM', start='2015-1-2', actions=False)
Ford=yf.download('F',start='2018-1-2', actions=False)
Google=yf.download('GOOGL',start='2000-1-2', actions=False)
Boeing=yf.download('BA', start='2015-1-2', actions=False)
Heinz=yf.download('KHC', actions=False)
Apple=yf.download('AAPL', start='2015-1-2', actions=False)
Facebook=yf.download('FB',start='2000-1-2', actions=False)
Netflix=yf.download('NFLX',start='2018-1-2', actions=False)
Nasdaq=yf.download('^IXIC', start='2015-1-2', actions=False)
Costco=yf.download('COST',start='2018-1-2', actions=False)
Uber=yf.download('UBER', actions=False)
Microsoft=yf.download('MSFT', start='2015-1-2', actions=False)
Amazon=yf.download('AMZN', start='2018-10-1', actions=False)
Zoom=yf.download('ZM', actions=False)
Tesla=yf.download('TSLA', actions=False)

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
    final_preds = final[-365:]
    num_final = final[0]
    num_initial = data['Close'].iloc[0]
    constant = (num_initial/num_final)
    
    preds = final_preds * constant
    preds = [round(num, 2) for num in preds]
    maximum = preds.index(np.max(preds))
    minimum = preds.index(np.min(preds))
    
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    current = yf.download('AAPL', start=current_date)
    current = current['Close'].values.tolist()
    current = current[0]
    current = math.ceil(current * 100) / 100
    
    stock_dictionary = {
              "preds": preds,
              "max": maximum,
              "min": minimum,
              "current": current
          
        }
    
    stocks[stock_name] = stock_dictionary
    fig=plt.figure()
    plt.figure(figsize=(40, 30))
    plt.plot(final[:len(final)])
    plt.plot(final[0:len(final)-365])
    plt.savefig(folder_path + stock_name) #save as png
         
train_send("zoom",Zoom, 300, 0)
train_send("heinz",Heinz, -1, 0)
train_send("apple",Apple, -1, 0)
# train_send("tesla",Tesla, 580, 1500)
train_send("nasdaq",Nasdaq, -1, 0)
train_send("amazon",Amazon, -1, 0)
#will add more

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