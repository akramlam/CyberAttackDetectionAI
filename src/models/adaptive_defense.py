import numpy as np
import tensorflow as tf
from collections import deque
import random
from typing import List, Dict, Tuple

class AdaptiveDefenseAgent:
    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        
    def _build_model(self):
        """Neural Net for Deep Q-learning Model"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))
        return model
        
    def remember(self, state: np.ndarray, action: int, reward: float, 
                next_state: np.ndarray, done: bool) -> None:
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
        
    def act(self, state: np.ndarray) -> int:
        """Choose action based on state"""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
        
    def replay(self, batch_size: int) -> float:
        """Train on past experiences"""
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return target

class AdaptiveDefenseSystem:
    def __init__(self):
        # State: [packet_rate, avg_packet_size, unique_ips, alert_rate, threat_score]
        self.state_size = 5
        # Actions: [block_ip, increase_monitoring, alert_admin, normal_operation]
        self.action_size = 4
        self.agent = AdaptiveDefenseAgent(self.state_size, self.action_size)
        self.action_map = {
            0: 'block_ip',
            1: 'increase_monitoring',
            2: 'alert_admin',
            3: 'normal_operation'
        }
        
    def get_state(self, metrics: Dict) -> np.ndarray:
        """Convert current system metrics to state vector"""
        state = np.array([
            metrics['packet_rate'],
            metrics['avg_packet_size'],
            metrics['unique_ips'],
            metrics['alert_rate'],
            metrics['threat_score']
        ])
        return np.reshape(state, [1, self.state_size])
        
    def get_reward(self, metrics: Dict, action: int) -> float:
        """Calculate reward based on action and resulting metrics"""
        reward = 0
        
        # Penalize unnecessary blocking
        if action == 0 and metrics['threat_score'] < 0.5:
            reward -= 10
            
        # Reward successful threat mitigation
        if metrics['threat_score'] > 0.7 and action in [0, 2]:
            reward += 20
            
        # Small penalty for unnecessary alerts
        if action == 2 and metrics['threat_score'] < 0.3:
            reward -= 5
            
        return reward
        
    def decide_action(self, current_metrics: Dict) -> str:
        """Decide next action based on current system state"""
        state = self.get_state(current_metrics)
        action = self.agent.act(state)
        return self.action_map[action]
        
    def learn_from_outcome(self, old_metrics: Dict, action: int, 
                          new_metrics: Dict, done: bool) -> None:
        """Learn from the outcome of actions"""
        old_state = self.get_state(old_metrics)
        new_state = self.get_state(new_metrics)
        reward = self.get_reward(new_metrics, action)
        
        self.agent.remember(old_state, action, reward, new_state, done)
        
        if len(self.agent.memory) > 32:
            self.agent.replay(32) 