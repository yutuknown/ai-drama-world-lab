"""
PPO (Proximal Policy Optimization) trainer for agents
Simplified implementation for demonstration
"""
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import List, Dict, Any
from collections import deque


class PPONetwork(nn.Module):
    """Simple neural network for PPO policy and value"""
    
    def __init__(self, observation_dim: int, action_dim: int, hidden_dim: int = 64):
        super().__init__()
        
        # Shared feature extraction
        self.shared = nn.Sequential(
            nn.Linear(observation_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Policy head (actor)
        self.policy = nn.Sequential(
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Output in [-1, 1]
        )
        
        # Value head (critic)
        self.value = nn.Linear(hidden_dim, 1)
        
    def forward(self, x):
        features = self.shared(x)
        action = self.policy(features)
        value = self.value(features)
        return action, value


class PPOTrainer:
    """
    PPO trainer for agent learning
    Simplified version for demonstration
    """
    
    def __init__(
        self,
        observation_dim: int,
        action_dim: int = 3,  # [move_x, move_z, action_type]
        learning_rate: float = 0.0003,
        gamma: float = 0.99,
        epsilon: float = 0.2,
        device: str = "cpu"
    ):
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.device = device
        
        # Create network
        self.network = PPONetwork(observation_dim, action_dim).to(device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=learning_rate)
        
        # Training buffer
        self.buffer = {
            "observations": [],
            "actions": [],
            "rewards": [],
            "values": [],
            "log_probs": [],
            "dones": []
        }
        
        # Training statistics
        self.training_steps = 0
        self.episode_rewards = deque(maxlen=100)
        
    def select_action(self, observation: np.ndarray) -> tuple:
        """
        Select action using current policy
        Returns (action, log_prob, value)
        """
        with torch.no_grad():
            obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)
            action, value = self.network(obs_tensor)
            
            # Add exploration noise
            action = action.cpu().numpy()[0]
            noise = np.random.normal(0, 0.1, size=action.shape)
            action = np.clip(action + noise, -1, 1)
            
            return action, 0.0, value.item()  # Simplified log_prob
    
    def store_transition(
        self,
        observation: np.ndarray,
        action: np.ndarray,
        reward: float,
        value: float,
        log_prob: float,
        done: bool
    ):
        """Store a transition in the buffer"""
        self.buffer["observations"].append(observation)
        self.buffer["actions"].append(action)
        self.buffer["rewards"].append(reward)
        self.buffer["values"].append(value)
        self.buffer["log_probs"].append(log_prob)
        self.buffer["dones"].append(done)
    
    def compute_returns(self) -> np.ndarray:
        """Compute discounted returns"""
        returns = []
        R = 0
        
        for reward, done in zip(
            reversed(self.buffer["rewards"]),
            reversed(self.buffer["dones"])
        ):
            if done:
                R = 0
            R = reward + self.gamma * R
            returns.insert(0, R)
        
        returns = np.array(returns)
        # Normalize returns
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        return returns
    
    def update(self) -> Dict[str, float]:
        """
        Update policy using PPO
        Returns training metrics
        """
        if len(self.buffer["observations"]) < 10:
            return {"loss": 0.0}
        
        # Prepare data
        observations = torch.FloatTensor(np.array(self.buffer["observations"])).to(self.device)
        actions = torch.FloatTensor(np.array(self.buffer["actions"])).to(self.device)
        returns = torch.FloatTensor(self.compute_returns()).to(self.device)
        old_values = torch.FloatTensor(self.buffer["values"]).to(self.device)
        
        # Multiple epochs of optimization
        for _ in range(4):
            # Forward pass
            pred_actions, pred_values = self.network(observations)
            pred_values = pred_values.squeeze()
            
            # Compute advantages
            advantages = returns - old_values.detach()
            
            # Policy loss (simplified)
            policy_loss = -(advantages.detach() * torch.sum((pred_actions - actions) ** 2, dim=1)).mean()
            
            # Value loss
            value_loss = nn.MSELoss()(pred_values, returns)
            
            # Total loss
            loss = policy_loss + 0.5 * value_loss
            
            # Optimization step
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.network.parameters(), 0.5)
            self.optimizer.step()
        
        self.training_steps += 1
        
        # Clear buffer
        metrics = {
            "loss": loss.item(),
            "policy_loss": policy_loss.item(),
            "value_loss": value_loss.item(),
            "mean_return": returns.mean().item()
        }
        
        self.clear_buffer()
        return metrics
    
    def clear_buffer(self):
        """Clear the experience buffer"""
        for key in self.buffer:
            self.buffer[key].clear()
    
    def save_checkpoint(self, path: str):
        """Save model checkpoint"""
        torch.save({
            "network_state": self.network.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
            "training_steps": self.training_steps
        }, path)
    
    def load_checkpoint(self, path: str):
        """Load model checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)
        self.network.load_state_dict(checkpoint["network_state"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state"])
        self.training_steps = checkpoint["training_steps"]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get training statistics"""
        return {
            "training_steps": self.training_steps,
            "buffer_size": len(self.buffer["observations"]),
            "avg_episode_reward": np.mean(self.episode_rewards) if self.episode_rewards else 0.0
        }
