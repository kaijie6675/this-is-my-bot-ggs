import unittest
from src.agent.ddpg_agent import DDPGAgent
import numpy as np

class TestDDPGAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DDPGAgent(state_dim=10, action_dim=4, max_action=1)

    def test_select_action(self):
        state = np.random.rand(10)
        action = self.agent.select_action(state)
        self.assertEqual(action.shape, (4,))

    def test_train(self):
        state = np.random.rand(64, 10)
        action = np.random.rand(64, 4)
        reward = np.random.rand(64, 1)
        next_state = np.random.rand(64, 10)
        done = np.random.randint(0, 2, size=(64, 1))
        
        self.agent.replay_buffer.add(state, action, reward, next_state, done)
        self.agent.train()

if __name__ == '__main__':
    unittest.main()