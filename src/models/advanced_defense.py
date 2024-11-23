import torch
import torch.nn as nn
import torch.optim as optim
from collections import namedtuple, deque
import random
import numpy as np
from typing import List, Tuple, Dict

Experience = namedtuple('Experience', ('state', 'action', 'reward', 'next_state', 'done'))

class DuelingDQN(nn.Module):
    def __init__(self, state_size: int, action_size: int):
        super(DuelingDQN, self).__init__()
        
        # Feature layer
        self.feature_layer = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )
        
        # Value stream
        self.value_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        # Advantage stream
        self.advantage_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )
        
    def forward(self, state):
        features = self.feature_layer(state)
        
        value = self.value_stream(features)
        advantages = self.advantage_stream(features)
        
        # Combine value and advantages
        qvals = value + (advantages - advantages.mean())
        return qvals

class AdvancedDefenseAgent:
    def __init__(self, state_size: int, action_size: int):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.state_size = state_size
        self.action_size = action_size
        
        # Networks
        self.policy_net = DuelingDQN(state_size, action_size).to(self.device)
        self.target_net = DuelingDQN(state_size, action_size).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        # Training parameters
        self.optimizer = optim.Adam(self.policy_net.parameters())
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        self.gamma = 0.99
        self.tau = 0.001
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
    def store_experience(self, state, action, reward, next_state, done):
        """Store experience in replay memory"""
        self.memory.append(Experience(state, action, reward, next_state, done))
        
    def act(self, state):
        """Choose action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
            
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.policy_net(state)
            return q_values.argmax().item()
            
    def train(self):
        """Train the agent on a batch of experiences"""
        if len(self.memory) < self.batch_size:
            return
            
        # Sample batch
        batch = random.sample(self.memory, self.batch_size)
        batch = Experience(*zip(*batch))
        
        # Convert to tensors
        state_batch = torch.FloatTensor(batch.state).to(self.device)
        action_batch = torch.LongTensor(batch.action).to(self.device)
        reward_batch = torch.FloatTensor(batch.reward).to(self.device)
        next_state_batch = torch.FloatTensor(batch.next_state).to(self.device)
        done_batch = torch.FloatTensor(batch.done).to(self.device)
        
        # Compute Q values
        current_q_values = self.policy_net(state_batch).gather(1, action_batch.unsqueeze(1))
        next_q_values = self.target_net(next_state_batch).max(1)[0].detach()
        expected_q_values = reward_batch + self.gamma * next_q_values * (1 - done_batch)
        
        # Compute loss and update
        loss = nn.MSELoss()(current_q_values, expected_q_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update target network
        for target_param, policy_param in zip(
            self.target_net.parameters(), 
            self.policy_net.parameters()
        ):
            target_param.data.copy_(
                self.tau * policy_param.data + (1 - self.tau) * target_param.data
            )
            
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        return loss.item() 