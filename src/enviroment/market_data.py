import requests
import pandas as pd

def fetch_data(symbol, interval, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}&outputsize=full"
    response = requests.get(url)
    data = response.json()
    
    # Convert the data to a DataFrame
    df = pd.DataFrame.from_dict(data['Time Series (5min)'], orient='index')
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

# Example usage
api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
symbol = 'BTCUSD'
interval = '5min'
data = fetch_data(symbol, interval, api_key)
data.to_csv('data/raw/BTCUSD.csv')