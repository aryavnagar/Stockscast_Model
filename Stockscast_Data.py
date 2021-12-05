import requests
from datetime import date
from numpy import array
import dateutil.parser as dp
import json


limit = '25'
date = str(date.today())
api_url = f'https://api.polygon.io/v2/reference/news?published_utc={date}&limit={limit}&apiKey=BpYLj3XDxfQZfCGlB3OiySFQTzWPBIvK'
data = requests.get(api_url).json()

for x in range (data['count']):
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
  locals()["news" + str(x)] = {
                              "id": id,
                              "url": url,
                              "title": title,
                              "publisher": publisher,
                              "publishDate": parsed_api_publish_in_seconds,
                              "thumbnail": thumbnail,
                              "keywords": keywords,
                              "tickers": tickers
                              }

l = []
for i in range(data['count']):
    l.append(locals()["news" + str(i)]) 
    
dataAryan = {
    "stocks": {},
    "news": l,
    "pass": "dev-RZZjmCxk9tTuAHnZ"
}

dataAryanJson = json.dumps(dataAryan)
url = 'https://api.mittaldev.com/stocks-dev/updateStocks'

post = requests.post(url, dataAryanJson)
print(post)