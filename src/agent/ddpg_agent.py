import torch
import torch.nn.functional as F
from src.agent.actor import Actor
from src.agent.critic import Critic
from src.utils.replay_buffer import ReplayBuffer

class DDPGAgent:
    def __init__(self, state_dim, action_dim, max_action):
        self.actor = Actor(state_dim, action_dim, max_action).to('cuda')
        self.actor_target = Actor(state_dim, action_dim, max_action).to('cuda')
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters())

        self.critic = Critic(state_dim, action_dim).to('cuda')
        self.critic_target = Critic(state_dim, action_dim).to('cuda')
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters())

        self.replay_buffer = ReplayBuffer()
        self.max_action = max_action

    def select_action(self, state):
        state = torch.FloatTensor(state.reshape(1, -1)).to('cuda')
        return self.actor(state).cpu().data.numpy().flatten()

    def train(self, batch_size=64, discount=0.99, tau=0.005):
        state, action, reward, next_state, done = self.replay_buffer.sample(batch_size)

        # Critic update
        target_q = self.critic_target(next_state, self.actor_target(next_state))
        target_q = reward + ((1 - done) * discount * target_q).detach()

        current_q = self.critic(state, action)
        critic_loss = F.mse_loss(current_q, target_q)

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        # Actor update
        actor_loss = -self.critic(state, self.actor(state)).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # Update target networks
        for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)

        for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)