'use client';

import { useState } from 'react';
import { agentAPI, episodeAPI } from '@/lib/api';
import { useAppStore } from '@/store/appStore';

export default function SimulationController() {
  const { currentScene, agents, isSimulating, setSimulating, currentEpisodeId, setCurrentEpisode, updateAgent } = useAppStore();
  const [simulationTime, setSimulationTime] = useState(0);
  const [fps, setFps] = useState(10);

  const startSimulation = async () => {
    if (!currentScene || agents.length === 0) {
      alert('Please create a scene and at least one agent first');
      return;
    }

    try {
      // Start episode recording
      const response = await episodeAPI.start(
        `Simulation ${new Date().toLocaleString()}`,
        `Scene: ${currentScene.name}, Agents: ${agents.length}`
      );
      setCurrentEpisode(response.episode_id);
      setSimulating(true);
      setSimulationTime(0);
      alert('Simulation started!');
    } catch (error) {
      console.error('Error starting simulation:', error);
      alert('Failed to start simulation');
    }
  };

  const stopSimulation = async () => {
    try {
      if (currentEpisodeId) {
        await episodeAPI.end();
      }
      setSimulating(false);
      setCurrentEpisode(null);
      alert('Simulation stopped and episode saved!');
    } catch (error) {
      console.error('Error stopping simulation:', error);
      setSimulating(false);
    }
  };

  const stepSimulation = async () => {
    if (!currentScene) return;

    try {
      const worldState = {
        objects: currentScene.objects,
        agents: agents,
      };

      // Step all agents
      const agentPromises = agents.map(agent =>
        agentAPI.step(agent.id, worldState)
      );

      const results = await Promise.all(agentPromises);

      // Update agent states
      results.forEach(result => {
        if (result.agent_state) {
          updateAgent(result.agent_state.id, result.agent_state);
        }
      });

      // Log frame if recording
      if (currentEpisodeId) {
        await episodeAPI.logFrame(
          simulationTime,
          agents,
          worldState,
          []
        );
      }

      setSimulationTime(prev => prev + 1 / fps);
    } catch (error) {
      console.error('Error stepping simulation:', error);
    }
  };

  // Auto-step when simulating
  useState(() => {
    let interval: NodeJS.Timeout;
    if (isSimulating) {
      interval = setInterval(stepSimulation, 1000 / fps);
    }
    return () => clearInterval(interval);
  });

  return (
    <div className="simulation-controller">
      <h2>Simulation Control</h2>
      
      <div className="status">
        <div className="status-item">
          <span className="label">Status:</span>
          <span className={`value ${isSimulating ? 'active' : 'inactive'}`}>
            {isSimulating ? 'Running' : 'Stopped'}
          </span>
        </div>
        <div className="status-item">
          <span className="label">Time:</span>
          <span className="value">{simulationTime.toFixed(2)}s</span>
        </div>
        <div className="status-item">
          <span className="label">Scene:</span>
          <span className="value">{currentScene?.name || 'None'}</span>
        </div>
        <div className="status-item">
          <span className="label">Agents:</span>
          <span className="value">{agents.length}</span>
        </div>
      </div>

      <div className="controls">
        {!isSimulating ? (
          <button className="start" onClick={startSimulation}>
            Start Simulation
          </button>
        ) : (
          <>
            <button className="stop" onClick={stopSimulation}>
              Stop Simulation
            </button>
            <button className="step" onClick={stepSimulation}>
              Step Once
            </button>
          </>
        )}
      </div>

      <div className="settings">
        <label>
          FPS: {fps}
          <input
            type="range"
            min="1"
            max="60"
            value={fps}
            onChange={(e) => setFps(parseInt(e.target.value))}
            disabled={isSimulating}
          />
        </label>
      </div>

      <style jsx>{`
        .simulation-controller {
          padding: 20px;
          background: #2a2a3e;
          border-radius: 8px;
          color: white;
        }
        
        h2 {
          margin: 0 0 20px 0;
          color: #4ecdc4;
        }
        
        .status {
          background: #1a1a2e;
          padding: 15px;
          border-radius: 4px;
          margin-bottom: 20px;
        }
        
        .status-item {
          display: flex;
          justify-content: space-between;
          margin-bottom: 10px;
          font-size: 14px;
        }
        
        .status-item:last-child {
          margin-bottom: 0;
        }
        
        .label {
          color: #888;
        }
        
        .value {
          font-weight: bold;
          color: #b4b4b4;
        }
        
        .value.active {
          color: #4ecdc4;
        }
        
        .value.inactive {
          color: #6f6f6f;
        }
        
        .controls {
          display: flex;
          gap: 10px;
          margin-bottom: 20px;
        }
        
        button {
          flex: 1;
          padding: 12px;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .start {
          background: #4ecdc4;
          color: #1a1a2e;
        }
        
        .start:hover {
          background: #45b7d1;
        }
        
        .stop {
          background: #ff6b6b;
          color: white;
        }
        
        .stop:hover {
          background: #ff5252;
        }
        
        .step {
          background: #f7d794;
          color: #1a1a2e;
        }
        
        .step:hover {
          background: #f5cd79;
        }
        
        .settings {
          background: #1a1a2e;
          padding: 15px;
          border-radius: 4px;
        }
        
        label {
          display: block;
          font-size: 14px;
          color: #b4b4b4;
        }
        
        input[type="range"] {
          width: 100%;
          margin-top: 10px;
        }
      `}</style>
    </div>
  );
}
