import { create } from 'zustand';
import { WorldScene, AgentState } from '@/types';

interface AppState {
  currentScene: WorldScene | null;
  agents: AgentState[];
  isSimulating: boolean;
  currentEpisodeId: string | null;
  
  setScene: (scene: WorldScene) => void;
  addAgent: (agent: AgentState) => void;
  updateAgent: (agentId: string, updates: Partial<AgentState>) => void;
  removeAgent: (agentId: string) => void;
  setAgents: (agents: AgentState[]) => void;
  setSimulating: (isSimulating: boolean) => void;
  setCurrentEpisode: (episodeId: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentScene: null,
  agents: [],
  isSimulating: false,
  currentEpisodeId: null,
  
  setScene: (scene) => set({ currentScene: scene }),
  
  addAgent: (agent) => set((state) => ({
    agents: [...state.agents, agent]
  })),
  
  updateAgent: (agentId, updates) => set((state) => ({
    agents: state.agents.map(agent =>
      agent.id === agentId ? { ...agent, ...updates } : agent
    )
  })),
  
  removeAgent: (agentId) => set((state) => ({
    agents: state.agents.filter(agent => agent.id !== agentId)
  })),
  
  setAgents: (agents) => set({ agents }),
  
  setSimulating: (isSimulating) => set({ isSimulating }),
  
  setCurrentEpisode: (episodeId) => set({ currentEpisodeId: episodeId }),
}));
