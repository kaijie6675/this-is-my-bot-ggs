import sys
from src.agent.ddpg_agent import DDPGAgent
from src.agent.quantitative_agent import QuantitativeAgent
from src.strategies.mean_reversion import MeanReversionStrategy
from src.strategies.moving_average_crossover import MovingAverageCrossoverStrategy
from src.strategies.quantitative_scalping_strategy import QuantitativeScalpingStrategy
from src.environment.trading_env import TradingEnv
from src.utils.data_loader import load_data
from src.utils.news_api import NewsAPI

def main(strategy="DDPG"):
    symbols = ["BTCUSD", "ETH-USD", "SOL-USD", "AAPL", "TSLA", "NVDA", "USDJPY", "EURUSD", "GBPUSD", "AUDUSD", "USDCHF", "NDX", "GSPC"]
    api_key = "0a7dd38299ba487d944d08866158d290"
    from_date = "2025-01-01"
    to_date = "2025-01-04"
    news_api = NewsAPI(api_key)

    news_data = news_api.fetch_news(symbols, from_date, to_date)
    sentiment_scores = news_api.analyze_news_sentiment(news_data)

    for symbol in symbols:
        data_path = f'data/raw/{symbol}.csv'
        df = load_data(data_path)
        news_sentiment = sentiment_scores.get(symbol, [])

        # Initialize the trading environment
        initial_balance = 10000
        env = TradingEnv(df, initial_balance=initial_balance)

        # Initialize the agent or strategy based on the input
        state_dim = env.observation_space.shape[1]
        action_dim = env.action_space.n
        max_action = 1

        signals = None  # Placeholder for strategy signals

        if strategy == "DDPG":
            agent = DDPGAgent(state_dim, action_dim, max_action)
        elif strategy == "Quantitative":
            agent = QuantitativeAgent(state_dim, action_dim, max_action)
        elif strategy == "MeanReversion":
            strategy_instance = MeanReversionStrategy(window=20, threshold=1.5)
            signals = strategy_instance.execute_strategy(df, news_sentiment)
        elif strategy == "MovingAverageCrossover":
            strategy_instance = MovingAverageCrossoverStrategy(short_window=40, long_window=100)
            signals = strategy_instance.execute_strategy(df)
        elif strategy == "QuantitativeScalping":
            strategy_instance = QuantitativeScalpingStrategy()
            signals = strategy_instance.execute_strategy(df, news_sentiment)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        if signals is not None:
            # Process the signals and execute trades based on them
            for index, row in signals.iterrows():
                if row['signal'] == 1:
                    # Buy signal
                    env.buy(index, row['close'], strategy_instance.leverage)
                elif row['signal'] == -1:
                    # Sell signal
                    env.sell(index, row['close'], strategy_instance.leverage)

        # Training loop (if applicable)
        for episode in range(100):  # Example number of episodes
            state = env.reset()
            done = False

            while not done:
                action = agent.select_action(state)
                next_state, reward, done, _ = env.step(action)
                agent.replay_buffer.add(state, action, reward, next_state, done)
                agent.train()
                state = next_state

            env.render()

if __name__ == "__main__":
    # Get the strategy from command-line arguments or default to "DDPG"
    strategy = sys.argv[1] if len(sys.argv) > 1 else "DDPG"
    main(strategy)