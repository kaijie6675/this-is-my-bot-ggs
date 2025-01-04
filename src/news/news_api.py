import requests
from textblob import TextBlob # type: ignore

class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_news(self, symbols, from_date, to_date, language='en'):
        all_news = {}
        for symbol in symbols:
            query = symbol
            url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&language={language}&apiKey={self.api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                all_news[symbol] = response.json()['articles']
            else:
                print(f"Failed to fetch news for {symbol}: {response.status_code}")
                all_news[symbol] = []
        return all_news

    def analyze_news_sentiment(self, news_data):
        sentiment_scores = {}
        for symbol, articles in news_data.items():
            scores = [TextBlob(article['title']).sentiment.polarity for article in articles]
            sentiment_scores[symbol] = scores
        return sentiment_scores

# Example usage
if __name__ == "__main__":
    api_key = "0a7dd38299ba487d944d08866158d290"
    symbols = ["BTCUSD", "ETH-USD", "SOL-USD", "AAPL"]
    from_date = "2025-01-01"
    to_date = "2025-01-04"
    news_api = NewsAPI(api_key)
    news_data = news_api.fetch_news(symbols, from_date, to_date)
    
    for symbol, articles in news_data.items():
        print(f"News for {symbol}:")
        for article in articles:
            print(article['title'])
    
    sentiment_scores = news_api.analyze_news_sentiment(news_data)
    print(sentiment_scores)