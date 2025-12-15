"""
Agent management API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from agents.embodied_agent import EmbodiedAgent, AgentConfig, AgentState
from agents.ppo_trainer import PPOTrainer
import asyncio

router = APIRouter()

# Global agent storage
active_agents: Dict[str, EmbodiedAgent] = {}
agent_trainers: Dict[str, PPOTrainer] = {}


class CreateAgentRequest(BaseModel):
    """Request to create a new agent"""
    name: str
    goal: str
    personality: str = "neutral"
    position: Optional[List[float]] = None


class AgentActionRequest(BaseModel):
    """Request to make agent perform action"""
    agent_id: str
    action_type: str  # move, interact, rest


@router.post("/create", response_model=AgentState)
async def create_agent(request: CreateAgentRequest):
    """Create a new embodied agent"""
    try:
        config = AgentConfig(
            name=request.name,
            goal=request.goal,
            personality=request.personality
        )
        
        agent = EmbodiedAgent(config)
        
        if request.position:
            import numpy as np
            agent.position = np.array(request.position)
        
        active_agents[agent.id] = agent
        
        # Create trainer for this agent
        trainer = PPOTrainer(observation_dim=29, action_dim=3)
        agent_trainers[agent.id] = trainer
        
        return agent.get_state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")


@router.get("/list", response_model=List[AgentState])
async def list_agents():
    """List all active agents"""
    return [agent.get_state() for agent in active_agents.values()]


@router.get("/{agent_id}", response_model=AgentState)
async def get_agent(agent_id: str):
    """Get specific agent state"""
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return active_agents[agent_id].get_state()


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    del active_agents[agent_id]
    if agent_id in agent_trainers:
        del agent_trainers[agent_id]
    
    return {"message": "Agent deleted successfully"}


@router.post("/{agent_id}/step")
async def step_agent(agent_id: str, world_state: Dict[str, Any]):
    """
    Execute one step of agent simulation
    Agent perceives world, decides action, and acts
    """
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        agent = active_agents[agent_id]
        trainer = agent_trainers.get(agent_id)
        
        # Perceive
        observation = agent.perceive(world_state)
        
        # Decide action (using trainer if available)
        if trainer:
            action_vector, log_prob, value = trainer.select_action(observation)
            # Convert action vector to action dict
            action = {
                "type": "move" if abs(action_vector[0]) > 0.1 or abs(action_vector[1]) > 0.1 else "idle",
                "movement": [action_vector[0] * 5, 0, action_vector[1] * 5],
                "name": "moving" if abs(action_vector[0]) > 0.1 or abs(action_vector[1]) > 0.1 else "idle"
            }
        else:
            action = agent.decide_action(observation)
        
        # Act
        agent.act(action)
        
        # Calculate reward
        reward = agent.calculate_reward(world_state)
        
        # Store experience in trainer
        if trainer:
            next_observation = agent.perceive(world_state)
            trainer.store_transition(observation, action_vector, reward, value, log_prob, False)
        
        # Store in agent memory
        agent.memory.add_experience(observation, action, reward, observation, False)
        agent.update_emotional_state()
        
        return {
            "agent_state": agent.get_state(),
            "action": action,
            "reward": reward
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stepping agent: {str(e)}")


@router.post("/{agent_id}/train")
async def train_agent(agent_id: str):
    """Trigger training update for agent"""
    if agent_id not in agent_trainers:
        raise HTTPException(status_code=404, detail="Agent trainer not found")
    
    try:
        trainer = agent_trainers[agent_id]
        metrics = trainer.update()
        return {
            "message": "Training update completed",
            "metrics": metrics,
            "stats": trainer.get_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training agent: {str(e)}")


@router.post("/{agent_id}/reset")
async def reset_agent(agent_id: str):
    """Reset agent to initial state"""
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    active_agents[agent_id].reset()
    return {"message": "Agent reset successfully"}
