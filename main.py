import requests
import itertools
import smtplib

# Input your interested stock and company name
STOCK = "JNJ"
COMPANY_NAME = "Johnson & Johnson"

# Input API key of Alphavantage
API_KEY_PRICE = # Input API KEY

# Input API key of Newsapi
API_KEY_NEWS = # Input API KEY

# Input username and password of email account
USER = # Input email address
PASSWORD = # Input password

# Retrieving stock price data from Alphavantage website
parameters_price = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_PRICE
}
response_price = requests.get(url="https://www.alphavantage.co/query", params=parameters_price)
response_price.raise_for_status()
price_data = response_price.json()
price_data_daily = dict(itertools.islice(price_data["Time Series (Daily)"].items(), 2))

yesterday = list(price_data_daily.keys())[0]
before_yesterday = list(price_data_daily.keys())[-1]

price_yesterday = float(price_data_daily[yesterday]["4. close"])
price_before_yesterday = float(price_data_daily[before_yesterday]["4. close"])

# Determine price difference between yesterday and the day before yesterday
price_difference = round(((price_yesterday - price_before_yesterday) / price_yesterday) * 100, 2)

# In case of price difference more than 5%,
if abs(price_difference) > 5:
    parameters_news = {
        "apiKey": API_KEY_NEWS,
        "language": "en",
        "q": f"{COMPANY_NAME}",
    }
# Retrieving related news about the stock
    response_news = requests.get(url="https://newsapi.org/v2/everything", params=parameters_news)
    response_news.raise_for_status()

# Send email about price alert with no related news
    if response_news.json()["totalResults"] == 0:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=USER, password=PASSWORD)
            connection.sendmail(
                from_addr=USER,
                to_addrs="thitipython@outlook.com",
                msg=f"Subject:{STOCK}: {price_difference}%\n\nNo related news"
            )
# Send email about price alert with top 3 related news
    else:
        news_data = response_news.json()["articles"][:3]
        for news in news_data:
            news_headline = news["title"]
            news_description = news["description"]
            print(f"Subject:{STOCK}: {price_difference}%\n\nHeadline: {news_headline}\n{news_description}")
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=USER, password=PASSWORD)
                connection.sendmail(
                    from_addr=USER,
                    to_addrs="thitipython@outlook.com",
                    msg=f"Subject:{STOCK}: {price_difference}%\n\nHeadline: {news_headline}\n{news_description}\n"
                )

