import gym
from gym import spaces
import numpy as np
import pandas as pd

class TradingEnv(gym.Env):
    def __init__(self, df, initial_balance=10000, lookback_window_size=50):
        super(TradingEnv, self).__init__()

        self.df = df
        self.initial_balance = initial_balance
        self.lookback_window_size = lookback_window_size

        self.action_space = spaces.Discrete(3)  # Buy, Sell, Hold
        self.observation_space = spaces.Box(low=0, high=1, shape=(lookback_window_size, len(df.columns) + 1), dtype=np.float16)

    def reset(self):
        self.balance = self.initial_balance
        self.net_worth = self.initial_balance
        self.max_net_worth = self.initial_balance
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        self.current_step = self.lookback_window_size
        return self._next_observation()

    def _next_observation(self):
        frame = np.array([
            self.df.loc[self.current_step - self.lookback_window_size:self.current_step, 'open'].values,
            self.df.loc[self.current_step - self.lookback_window_size:self.current_step, 'high'].values,
            self.df.loc[self.current_step - self.lookback_window_size:self.current_step, 'low'].values,
            self.df.loc[self.current_step - self.lookback_window_size:self.current_step, 'close'].values,
            self.df.loc[self.current_step - self.lookback_window_size:self.current_step, 'volume'].values,
        ])

        obs = np.append(frame, [[self.balance], [self.net_worth], [self.shares_held], [self.cost_basis]], axis=0)
        return obs

    def step(self, action):
        self._take_action(action)
        self.current_step += 1

        if self.current_step > len(self.df) - 1:
            self.current_step = self.lookback_window_size

        reward = self.net_worth - self.initial_balance
        done = self.net_worth <= 0

        obs = self._next_observation()
        return obs, reward, done, {}

    def _take_action(self, action):
        current_price = self.df.loc[self.current_step, 'close']
        if action == 0:  # Buy
            shares_bought = self.balance // current_price
            self.balance -= shares_bought * current_price
            self.shares_held += shares_bought
            self.cost_basis = current_price
        elif action == 1:  # Sell
            self.balance += self.shares_held * current_price
            self.shares_held = 0
        elif action == 2:  # Hold
            pass  # Do nothing

        self.net_worth = self.balance + self.shares_held * current_price
        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

    def render(self, mode='human', close=False):
        profit = self.net_worth - self.initial_balance
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held} (Total sold: {self.total_shares_sold})')
        print(f'Net worth: {self.net_worth} (Max net worth: {self.max_net_worth})')
        print(f'Profit: {profit}')