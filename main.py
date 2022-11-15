from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY = Deleted for security
NEWS_API_KEY = Deleted for security
account_sid = Deleted for security
auth_token = Deleted for security
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

import requests

parameters = {
    "symbol": STOCK_NAME,
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "apikey": ALPHA_API_KEY

}

response = requests.get(STOCK_ENDPOINT, params=parameters)

data = response.json()["Time Series (Daily)"]

last_2 = [float(item['4. close']) for key,item in data.items()][:2]
print(last_2)

difference = abs(round(last_2[0] - last_2[1], 2))


percent_difference = round(difference / max(last_2) * 100, 2)

gain_loss = "Up"

if last_2[0] < last_2[1]:
    percent_difference = -abs(percent_difference)
    gain_loss = "Down"

news_params = {
    "q": COMPANY_NAME,
    "sortBy": "publishedAt",
    "apiKey": NEWS_API_KEY,
    "pageSize": 3,
    "searchIn": "description"
}

if percent_difference > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params).json()["articles"]
    headlines = [item["title"] for item in news_response]
    summary = [item["description"] for item in news_response]


    client = Client(account_sid, auth_token)
    for number in range(3):
        message = client.messages.create(
            body=f"{COMPANY_NAME} is {gain_loss} {percent_difference}% \nHeadline: {headlines[number]}\nBrief: {summary[number]}",
            from_='13396752740',
            to='+13216145471'
        )

        print(message.status)
