"""
Embodied agent base class with memory and learning capabilities
"""
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field
import numpy as np
from collections import deque
import uuid


class AgentMemory:
    """Agent memory system for storing experiences"""
    
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.short_term = deque(maxlen=100)  # Recent experiences
        self.long_term = deque(maxlen=capacity)  # All experiences
        self.episodic = []  # Episode-specific memories
        
    def add_experience(self, observation: np.ndarray, action: Any, 
                      reward: float, next_observation: np.ndarray, 
                      done: bool):
        """Add an experience to memory"""
        experience = {
            "observation": observation,
            "action": action,
            "reward": reward,
            "next_observation": next_observation,
            "done": done
        }
        self.short_term.append(experience)
        self.long_term.append(experience)
        
    def add_episodic_memory(self, event: Dict[str, Any]):
        """Add episodic memory (significant events)"""
        self.episodic.append(event)
        
    def get_recent(self, n: int = 10) -> List[Dict]:
        """Get n most recent experiences"""
        return list(self.short_term)[-n:]
    
    def clear_episodic(self):
        """Clear episodic memory (e.g., at episode end)"""
        self.episodic.clear()
        
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "short_term_size": len(self.short_term),
            "long_term_size": len(self.long_term),
            "episodic_size": len(self.episodic)
        }


class AgentConfig(BaseModel):
    """Agent configuration"""
    name: str
    goal: str
    personality: str = "neutral"
    learning_rate: float = 0.0003
    max_speed: float = 5.0
    observation_radius: float = 10.0
    
    
class AgentState(BaseModel):
    """Current state of an agent"""
    id: str
    name: str
    position: List[float] = Field(default_factory=lambda: [0, 0.5, 0])
    velocity: List[float] = Field(default_factory=lambda: [0, 0, 0])
    rotation: float = 0.0
    health: float = 100.0
    energy: float = 100.0
    goal: str = ""
    current_action: str = "idle"
    emotional_state: str = "neutral"
    
    
class EmbodiedAgent:
    """
    Embodied agent with perception, action, and learning capabilities
    Uses PPO for learning (simplified version)
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.id = str(uuid.uuid4())
        self.memory = AgentMemory()
        
        # State
        self.position = np.array([0.0, 0.5, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation = 0.0
        
        # Agent properties
        self.health = 100.0
        self.energy = 100.0
        self.current_action = "idle"
        self.emotional_state = "neutral"
        
        # Learning parameters
        self.total_reward = 0.0
        self.episode_steps = 0
        
    def perceive(self, world_state: Dict[str, Any]) -> np.ndarray:
        """
        Perceive the world and create observation
        Returns a feature vector representing what the agent sees
        """
        # Simplified observation: relative positions of nearby objects
        observation = []
        
        # Agent's own state
        observation.extend(self.position.tolist())
        observation.extend(self.velocity.tolist())
        observation.append(self.rotation)
        observation.append(self.health / 100.0)
        observation.append(self.energy / 100.0)
        
        # Nearby objects (simplified - in production, use spatial queries)
        objects = world_state.get("objects", [])
        nearby_objects = []
        
        for obj in objects[:5]:  # Consider up to 5 nearest objects
            if "position" in obj:
                obj_pos = np.array(obj["position"])
                relative_pos = obj_pos - self.position
                distance = np.linalg.norm(relative_pos)
                
                if distance < self.config.observation_radius:
                    nearby_objects.extend(relative_pos.tolist())
                    nearby_objects.append(distance)
        
        # Pad observation to fixed size
        while len(nearby_objects) < 20:  # 5 objects * 4 features
            nearby_objects.append(0.0)
        
        observation.extend(nearby_objects[:20])
        
        return np.array(observation, dtype=np.float32)
    
    def decide_action(self, observation: np.ndarray) -> Dict[str, Any]:
        """
        Decide action based on observation
        In production, this would use a trained PPO policy network
        """
        # Simplified action selection (random exploration + some logic)
        
        # Decrease energy over time
        self.energy = max(0, self.energy - 0.1)
        
        # Low energy -> rest
        if self.energy < 20:
            return {
                "type": "rest",
                "movement": [0, 0, 0],
                "name": "resting"
            }
        
        # Random movement with some goal-directed behavior
        action_type = np.random.choice(["move", "interact", "idle"], p=[0.7, 0.2, 0.1])
        
        if action_type == "move":
            # Random direction with some momentum
            direction = np.random.randn(3)
            direction[1] = 0  # No vertical movement
            direction = direction / (np.linalg.norm(direction) + 1e-8)
            
            speed = np.random.uniform(0.5, self.config.max_speed)
            movement = direction * speed
            
            return {
                "type": "move",
                "movement": movement.tolist(),
                "name": "moving"
            }
        elif action_type == "interact":
            return {
                "type": "interact",
                "movement": [0, 0, 0],
                "name": "interacting"
            }
        else:
            return {
                "type": "idle",
                "movement": [0, 0, 0],
                "name": "idle"
            }
    
    def act(self, action: Dict[str, Any], dt: float = 0.016):
        """Execute action and update agent state"""
        self.current_action = action.get("name", "idle")
        
        if action["type"] == "move":
            movement = np.array(action["movement"])
            self.velocity = movement
            self.position += self.velocity * dt
            
            # Update rotation based on movement direction
            if np.linalg.norm(movement) > 0.01:
                self.rotation = np.arctan2(movement[2], movement[0])
            
            self.energy = max(0, self.energy - 0.2)
            
        elif action["type"] == "rest":
            self.velocity = np.array([0, 0, 0])
            self.energy = min(100, self.energy + 1.0)
            
        elif action["type"] == "interact":
            self.velocity = np.array([0, 0, 0])
            self.energy = max(0, self.energy - 0.5)
        
        self.episode_steps += 1
        
    def calculate_reward(self, world_state: Dict[str, Any]) -> float:
        """
        Calculate reward based on current state and world
        This drives learning
        """
        reward = 0.0
        
        # Reward for staying alive
        reward += 0.1
        
        # Penalty for low energy
        if self.energy < 20:
            reward -= 0.5
        
        # Small penalty for being idle (encourage exploration)
        if self.current_action == "idle":
            reward -= 0.05
        
        # Reward for interacting
        if self.current_action == "interacting":
            reward += 0.3
        
        # Keep agent in bounds (simple boundary)
        distance_from_center = np.linalg.norm(self.position[[0, 2]])
        if distance_from_center > 10:
            reward -= 1.0
        
        self.total_reward += reward
        return reward
    
    def update_emotional_state(self):
        """Update emotional state based on recent experiences"""
        recent = self.memory.get_recent(n=10)
        
        if not recent:
            self.emotional_state = "neutral"
            return
        
        avg_reward = np.mean([exp["reward"] for exp in recent])
        
        if avg_reward > 0.2:
            self.emotional_state = "happy"
        elif avg_reward < -0.2:
            self.emotional_state = "frustrated"
        else:
            self.emotional_state = "neutral"
    
    def get_state(self) -> AgentState:
        """Get current agent state for serialization"""
        return AgentState(
            id=self.id,
            name=self.config.name,
            position=self.position.tolist(),
            velocity=self.velocity.tolist(),
            rotation=float(self.rotation),
            health=self.health,
            energy=self.energy,
            goal=self.config.goal,
            current_action=self.current_action,
            emotional_state=self.emotional_state
        )
    
    def reset(self, position: Optional[np.ndarray] = None):
        """Reset agent to initial state"""
        if position is not None:
            self.position = position.copy()
        else:
            self.position = np.array([0.0, 0.5, 0.0])
        
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.rotation = 0.0
        self.health = 100.0
        self.energy = 100.0
        self.current_action = "idle"
        self.emotional_state = "neutral"
        self.total_reward = 0.0
        self.episode_steps = 0
        self.memory.clear_episodic()
