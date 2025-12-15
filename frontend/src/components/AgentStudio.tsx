'use client';

import { useState } from 'react';
import { agentAPI } from '@/lib/api';
import { useAppStore } from '@/store/appStore';

export default function AgentStudio() {
  const [name, setName] = useState('');
  const [goal, setGoal] = useState('');
  const [personality, setPersonality] = useState('neutral');
  const [loading, setLoading] = useState(false);
  const { agents, addAgent, removeAgent } = useAppStore();

  const handleCreateAgent = async () => {
    if (!name.trim() || !goal.trim()) {
      alert('Please provide both name and goal');
      return;
    }
    
    setLoading(true);
    try {
      const agent = await agentAPI.create(name, goal, personality);
      addAgent(agent);
      setName('');
      setGoal('');
      alert(`Agent "${agent.name}" created successfully!`);
    } catch (error) {
      console.error('Error creating agent:', error);
      alert('Failed to create agent. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAgent = async (agentId: string) => {
    try {
      await agentAPI.delete(agentId);
      removeAgent(agentId);
    } catch (error) {
      console.error('Error deleting agent:', error);
      alert('Failed to delete agent.');
    }
  };

  return (
    <div className="agent-studio">
      <h2>Agent Studio</h2>
      <p>Create and manage AI agents</p>
      
      <div className="create-form">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Agent name..."
          disabled={loading}
        />
        
        <input
          type="text"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Agent goal (e.g., 'Explore the world')..."
          disabled={loading}
        />
        
        <select
          value={personality}
          onChange={(e) => setPersonality(e.target.value)}
          disabled={loading}
        >
          <option value="neutral">Neutral</option>
          <option value="curious">Curious</option>
          <option value="cautious">Cautious</option>
          <option value="bold">Bold</option>
        </select>
        
        <button onClick={handleCreateAgent} disabled={loading}>
          {loading ? 'Creating...' : 'Create Agent'}
        </button>
      </div>
      
      <div className="agents-list">
        <h3>Active Agents ({agents.length})</h3>
        {agents.length === 0 ? (
          <p className="empty">No agents created yet</p>
        ) : (
          agents.map((agent) => (
            <div key={agent.id} className="agent-card">
              <div className="agent-info">
                <strong>{agent.name}</strong>
                <span className="goal">{agent.goal}</span>
                <div className="stats">
                  <span className="stat">Action: {agent.current_action}</span>
                  <span className="stat">Energy: {agent.energy.toFixed(1)}%</span>
                  <span className={`emotion ${agent.emotional_state}`}>
                    {agent.emotional_state}
                  </span>
                </div>
              </div>
              <button
                className="delete-btn"
                onClick={() => handleDeleteAgent(agent.id)}
              >
                Delete
              </button>
            </div>
          ))
        )}
      </div>

      <style jsx>{`
        .agent-studio {
          padding: 20px;
          background: #2a2a3e;
          border-radius: 8px;
          color: white;
        }
        
        h2 {
          margin: 0 0 10px 0;
          color: #4ecdc4;
        }
        
        p {
          margin: 0 0 20px 0;
          color: #b4b4b4;
        }
        
        .create-form {
          margin-bottom: 30px;
        }
        
        input, select {
          width: 100%;
          padding: 12px;
          margin-bottom: 10px;
          border: 2px solid #3a3a4e;
          border-radius: 4px;
          background: #1a1a2e;
          color: white;
          font-family: inherit;
          font-size: 14px;
        }
        
        input:focus, select:focus {
          outline: none;
          border-color: #4ecdc4;
        }
        
        button {
          width: 100%;
          padding: 12px 24px;
          background: #4ecdc4;
          color: #1a1a2e;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          transition: background 0.2s;
        }
        
        button:hover:not(:disabled) {
          background: #45b7d1;
        }
        
        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        .agents-list h3 {
          font-size: 16px;
          margin-bottom: 15px;
          color: #4ecdc4;
        }
        
        .empty {
          color: #6f6f6f;
          text-align: center;
          padding: 20px;
        }
        
        .agent-card {
          background: #1a1a2e;
          padding: 15px;
          border-radius: 4px;
          margin-bottom: 10px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .agent-info {
          flex: 1;
        }
        
        .agent-info strong {
          display: block;
          font-size: 16px;
          margin-bottom: 5px;
          color: #4ecdc4;
        }
        
        .goal {
          display: block;
          font-size: 13px;
          color: #b4b4b4;
          margin-bottom: 8px;
        }
        
        .stats {
          display: flex;
          gap: 12px;
          font-size: 12px;
        }
        
        .stat {
          color: #888;
        }
        
        .emotion {
          padding: 2px 8px;
          border-radius: 3px;
          font-weight: bold;
        }
        
        .emotion.happy {
          background: #4ecdc4;
          color: #1a1a2e;
        }
        
        .emotion.frustrated {
          background: #ff6b6b;
          color: white;
        }
        
        .emotion.neutral {
          background: #6f6f6f;
          color: white;
        }
        
        .delete-btn {
          width: auto;
          padding: 8px 16px;
          background: #ff6b6b;
          font-size: 14px;
        }
        
        .delete-btn:hover {
          background: #ff5252;
        }
      `}</style>
    </div>
  );
}
