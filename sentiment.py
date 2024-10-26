def sentiment(name):
    import requests
    import pandas as pd
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # Initialize VADER sentiment analyzer

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

    analyzer = SentimentIntensityAnalyzer()

    # Financial keywords for sentiment adjustment
    bullish_keywords = ["growth", "rise", "surge", "gain", "increase", "bullish"]
    bearish_keywords = ["decline", "drop", "fall", "loss", "decrease", "bearish"]

    # Function to fetch recent news articles for the cryptocurrency
    def fetch_crypto_news(coin_name, api_key="a79b195d7f9249eda6def81ff7e7c7c8"):
        url = f"https://newsapi.org/v2/everything?q={coin_name}&sortBy=publishedAt&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['articles']
        else:
            print("Failed to fetch news articles")
            print("Status Code:", response.status_code)
            print("Response:", response.json())
            return []

    # Function to analyze sentiment of each article headline with VADER and keyword adjustment
    def analyze_sentiment_vader(text):
        sentiment_score = analyzer.polarity_scores(text)['compound']
        
        # Keyword adjustments for financial context, now with a smaller adjustment factor
        for word in bullish_keywords:
            if word in text.lower():
                sentiment_score += 0.2  # Smaller influence
                break
        for word in bearish_keywords:
            if word in text.lower():
                sentiment_score -= 0.5  # Smaller influence
                break

        # Updated thresholds for bullish/bearish sentiment
        if sentiment_score > 0.3:
            return 1  # Bullish
        elif sentiment_score < -0.3:
            return -1  # Bearish
        else:
            return 0  # Neutral

    # Main analysis function
    def crypto_sentiment_analysis(coin_name):
        coin_name = get_crypto_ticker(coin_name)
        # Fetch recent news articles
        articles = fetch_crypto_news(coin_name)
        if not articles:
            print("No articles found.")
            return

        # Process and analyze sentiment of each article
        data = []
        for article in articles:
            headline = article['title']
            date = article['publishedAt'][:10]  # Extract date from timestamp
            sentiment_score = analyze_sentiment_vader(headline)
            sentiment = "Bullish" if sentiment_score == 1 else "Bearish" if sentiment_score == -1 else "Neutral"
            data.append({"date": date, "headline": headline, "sentiment_score": sentiment_score, "sentiment": sentiment})

        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Aggregate daily sentiment scores
        df['date'] = pd.to_datetime(df['date'])
        daily_sentiment = df.groupby(df['date'].dt.date)['sentiment_score'].sum().reset_index()
        daily_sentiment.columns = ['date', 'daily_sentiment_score']

        # Calculate cumulative sentiment score over the last 7 days
        cumulative_score = daily_sentiment['daily_sentiment_score'].sum()

        # Narrow down the final sentiment interpretation based on cumulative score
    # Revised cumulative sentiment interpretation function with higher bullish thresholds
        def interpret_cumulative_sentiment(score):
            if score >= 10:  # Higher boundary for Strongly Bullish
                return 'Strongly Bullish'
            elif 5 <= score < 10:  # Higher boundary for Bullish
                return 'Bullish'
            elif -2 < score < 5:  # Broaden Neutral range
                return 'Neutral'
            elif -4 < score <= -2:  # Higher boundary for Bearish
                return 'Bearish'
            else:
                return 'Strongly Bearish'


        # Determine overall 7-day sentiment
        seven_day_sentiment = interpret_cumulative_sentiment(cumulative_score)

        # Display detailed results
        # print("7-Day News Sentiment Analysis for", coin_name.capitalize())
        # print("============================================")
        # print("Date       | Headline                                         | Sentiment")
        # print("-----------|--------------------------------------------------|----------")
        for i, row in df.iterrows():
            if i == 98:
                finalheadline1 = row['headline'][:80]
            elif i == 99:
                finalheadline2 = row['headline'][:80]
                
            # print(f"{row['date']} | {row['headline'][:70]:<70} | {row['sentiment']}")

        # # Summary
        # print("\nSummary of the 7-Day Sentiment Analysis:")
        # print("============================================")
        # print(f"Cumulative Sentiment Score: {cumulative_score}")
        # print(f"Overall 7-Day Sentiment: {seven_day_sentiment}")
        return seven_day_sentiment

    # Run the analysis for Bitcoin (or any other cryptocurrency)
    try:
        return crypto_sentiment_analysis(name)
    except Exception as err:
        print("Error:", err)

input_front = ""
sentiment(input_front)
