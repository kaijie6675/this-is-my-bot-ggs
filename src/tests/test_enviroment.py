import unittest
import pandas as pd
from src.environment.trading_env import TradingEnv

class TestTradingEnv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        df = pd.read_csv('data/raw/BTCUSD.csv', index_col=0, parse_dates=True)
        cls.env = TradingEnv(df)

    def test_reset(self):
        obs = self.env.reset()
        self.assertEqual(obs.shape, (50, 6))

    def test_step(self):
        self.env.reset()
        obs, reward, done, _ = self.env.step(0)
        self.assertEqual(obs.shape, (50, 6))
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)

if __name__ == '__main__':
    unittest.main()