export interface Object3D {
  id: string;
  type: string;
  position: [number, number, number];
  rotation: [number, number, number];
  scale: [number, number, number];
  color: string;
  name?: string;
  properties?: Record<string, any>;
}

export interface WorldScene {
  id: string;
  name: string;
  description: string;
  objects: Object3D[];
  lighting: {
    ambient?: { color: string; intensity: number };
    directional?: { color: string; intensity: number; position: [number, number, number] };
  };
  physics_config: {
    gravity: [number, number, number];
    enabled: boolean;
  };
  metadata?: Record<string, any>;
}

export interface AgentState {
  id: string;
  name: string;
  position: [number, number, number];
  velocity: [number, number, number];
  rotation: number;
  health: number;
  energy: number;
  goal: string;
  current_action: string;
  emotional_state: string;
}

export interface Episode {
  episode_id: string;
  metadata: Record<string, any>;
  start_time: string;
  end_time?: string;
  num_frames: number;
}

export interface EpisodeFrame {
  timestamp: number;
  agents_state: AgentState[];
  world_state: any;
  events: any[];
}
