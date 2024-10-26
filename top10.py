def top10func():
    from pycoingecko import CoinGeckoAPI
    import pandas as pd

    # Initialize CoinGecko API
    cg = CoinGeckoAPI()

    # Fetch data for the top 10 coins by market cap
    top_coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1)

    # Extract relevant data: name, symbol, current price, market cap, and 1h change
    top_coins_data = []
    strs = ""
    for coin in top_coins:
        strs += "." + coin['name'] + "," + coin['symbol'] + "," + str(coin['current_price']) + "," + str(coin.get('price_change_percentage_24h'))
        top_coins_data.append({
            'Name': coin['name'],
            'Symbol': coin['symbol'],
            'Current Price (USD)': coin['current_price'],
            '24h Change (%)': coin.get('price_change_percentage_24h')
        })
    return strs

    #.name,ticker,currentPrice,%change
    
    
    # # Convert data to DataFrame for easy display
    # top_coins_df = pd.DataFrame(top_coins_data)
    # print(top_coins_df)