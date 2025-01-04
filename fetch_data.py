import requests
import os

def fetch_alpha_vantage_data(symbol, api_key, output_file):
    """Fetch historical data for a given symbol from Alpha Vantage and save as CSV."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact&datatype=csv"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, 'w') as file:
            file.write(response.text)
        print(f"Data for {symbol} saved to {output_file}")
    else:
        print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")

def main():
    # Your Alpha Vantage API key
    api_key = "W5HDCVKPBDRGQFMT"
    
    # Symbols to fetch data for
    symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "AAPL", "TSLA", "NVDA", "USDJPY", "EURUSD", "GBPUSD", "AUDUSD", "USDCHF", "NDX", "GSPC"]
    
    # Directory to save the CSV files
    output_dir = "data/raw/"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for symbol in symbols:
        output_file = os.path.join(output_dir, f"{symbol.replace('/', '_')}.csv")
        fetch_alpha_vantage_data(symbol, api_key, output_file)

if __name__ == "__main__":
    main()