def technical(name):
    import pandas as pd
    import requests
    import numpy as np
    from pycoingecko import CoinGeckoAPI
    def get_crypto_ticker(name):
        # Fetch the list of coins from CoinGecko API
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        coins = response.json()
        
        # Search for the coin by name and return its symbol
        for coin in coins:
            if coin['name'].lower() == name.lower():
                return coin['symbol'].upper()  # Returning the ticker in uppercase
        return None  # Return None if the coin name is not found

    # Initialize the CoinGecko API client
    cg = CoinGeckoAPI()

    # Parameters
    coin_id = 'bitcoin'  # Replace with the ID of any other coin as needed
    vs_currency = 'usd'
    days = '7'  # Analyze the last 7 days for trend analysis

    # Fetch historical data (prices only for simplicity)
    data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=vs_currency, days=days)

    # Convert to DataFrame
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Calculate daily returns (percentage change in price)
    df['daily_price_change'] = df['price'].pct_change() * 100  # in percentage

    # Define daily sentiment score based on daily price change
    def daily_sentiment_score(price_change):
        if price_change > 1:
            return 1  # Bullish
        elif price_change < -1:
            return -1  # Bearish
        else:
            return 0  # Neutral

    # Apply the daily sentiment scoring
    df['daily_sentiment_score'] = df['daily_price_change'].apply(daily_sentiment_score)

    # Calculate cumulative score to interpret 7-day trend
    cumulative_score = df['daily_sentiment_score'].sum()

    # Define sentiment based on cumulative score
    def interpret_cumulative_sentiment(score):
        if score >= 5:
            return 'Strongly Bullish'
        elif 2 <= score < 5:
            return 'Bullish'
        elif -2 < score < 2:
            return 'Neutral'
        elif -5 < score <= -2:
            return 'Bearish'
        else:
            return 'Strongly Bearish'

    # Determine the 7-day sentiment
    seven_day_sentiment = interpret_cumulative_sentiment(cumulative_score)

    # Display results
    # print("7-Day Trend Analysis for", coin_id.capitalize())
    # print("============================================")
    # print("Date       | Price       | Daily Change (%) | Daily Sentiment Score")
    # print("-----------|-------------|------------------|----------------------")

    for i, row in df.iterrows():
        if i == 168:
            date = row['timestamp'].strftime('%Y-%m-%d')
            price = f"${row['price']:.2f}"
            change = f"{row['daily_price_change']:.2f}%"
            score = row['daily_sentiment_score']
            sentiment = 'Bullish' if score == 1 else 'Bearish' if score == -1 else 'Neutral'
            # print(f"{date} | {price:<10} | {change:<16} | {sentiment}")

    # Final output: Overall sentiment based on the cumulative score
    # print("\nSummary of the 7-Day Sentiment Analysis:")
    # print("============================================")
    # print(f"Cumulative Sentiment Score: {cumulative_score}")
    # print(f"Overall 7-Day Sentiment: {seven_day_sentiment}")
    return f"{coin_id.capitalize()},{price:<5},{change:<5},{seven_day_sentiment}"
    # name, price, % change, overall sentiment
    
print(technical("bitcoin"))
