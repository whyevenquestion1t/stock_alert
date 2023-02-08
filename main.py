import requests
from datetime import *
import os
from twilio.rest import Client

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

PRICE_API_KEY = "XFVNF7SQKI7O1867"
NEWS_API = "fdb3dc6410c84b4e99bf702560ff9d56"
TWILLIO_API = "cb70268af02784cec6fea59326f6b42e"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": PRICE_API_KEY
}

url = "https://www.alphavantage.co/query"
r = requests.get(url=url, params=parameters)
data = r.json()

# date
yesterday = date.today() - timedelta(1)
datetime.strftime(yesterday, '%Y-%m-%d')
before_yesterday = date.today() - timedelta(6)
datetime.strftime(yesterday, '%Y-%m-%d')

# percentage difference
direction = None


def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


# json parsing and raising errors
try:
    price_yesterday = data["Time Series (Daily)"][str(yesterday)]["4. close"]
    price_before_yesterday = data["Time Series (Daily)"][str(before_yesterday)]["4. close"]

    difference = get_change(current=float(price_yesterday), previous=float(price_before_yesterday))


    if difference > 5:
        direction = True
        print("Get news")
    difference = ("%.2f" % difference)

except KeyError:
    print("Not enough data, the stock market was closed")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_url = "https://newsapi.org/v2/everything?"
parameters = {
    "q": STOCK,
    "from": str(yesterday),
    "sortBy": "popularity",
    "apiKey": NEWS_API,
}

article = requests.get(url=news_url, params=parameters)
article_data = article.json()
news = article_data["articles"][0]['description']
news_2 = article_data["articles"][1]["description"]
print(f"{news} \n{news_2}")


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

def send_SMS(direction):
    if direction:
        emoji = "⬆"
    else:
        emoji = "⬇️"
    return emoji


# api call
sign = send_SMS(direction)

account_sid = 'ACb8f0cfbfbb2c1cbce5fa6ddf06556f56'
auth_token = 'cb70268af02784cec6fea59326f6b42e'
client = Client(account_sid, auth_token)

message = client.messages.create(to='+19295037535', from_="+18559440731",
                                 body=f"{STOCK}: {sign}{difference}%\n1. {news}\n2. {news_2}")


