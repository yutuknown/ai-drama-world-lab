"""
Episode logging system for recording and replaying simulations
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import uuid


class EpisodeFrame:
    """Single frame of episode data"""
    
    def __init__(self, timestamp: float, agents_state: List[Dict], 
                 world_state: Dict, events: List[Dict] = None):
        self.timestamp = timestamp
        self.agents_state = agents_state
        self.world_state = world_state
        self.events = events or []
        
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "agents_state": self.agents_state,
            "world_state": self.world_state,
            "events": self.events
        }


class Episode:
    """Complete episode with metadata and frames"""
    
    def __init__(self, episode_id: str = None, metadata: Dict = None):
        self.episode_id = episode_id or str(uuid.uuid4())
        self.metadata = metadata or {}
        self.frames: List[EpisodeFrame] = []
        self.start_time = datetime.now()
        self.end_time = None
        
    def add_frame(self, frame: EpisodeFrame):
        """Add a frame to the episode"""
        self.frames.append(frame)
        
    def finalize(self):
        """Mark episode as complete"""
        self.end_time = datetime.now()
        
    def to_dict(self) -> Dict:
        """Convert episode to dictionary for serialization"""
        return {
            "episode_id": self.episode_id,
            "metadata": self.metadata,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "num_frames": len(self.frames),
            "frames": [frame.to_dict() for frame in self.frames]
        }
        
    def get_summary(self) -> Dict:
        """Get episode summary without frame data"""
        return {
            "episode_id": self.episode_id,
            "metadata": self.metadata,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "num_frames": len(self.frames),
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        }


class EpisodeLogger:
    """Manages episode recording and storage"""
    
    def __init__(self, storage_dir: str = "./episodes"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.current_episode: Optional[Episode] = None
        
    def start_episode(self, metadata: Dict = None) -> str:
        """Start a new episode"""
        self.current_episode = Episode(metadata=metadata)
        return self.current_episode.episode_id
        
    def log_frame(self, timestamp: float, agents_state: List[Dict],
                  world_state: Dict, events: List[Dict] = None):
        """Log a frame to the current episode"""
        if not self.current_episode:
            raise ValueError("No active episode. Call start_episode first.")
        
        frame = EpisodeFrame(timestamp, agents_state, world_state, events)
        self.current_episode.add_frame(frame)
        
    def end_episode(self) -> Dict:
        """End current episode and save to disk"""
        if not self.current_episode:
            raise ValueError("No active episode to end.")
        
        self.current_episode.finalize()
        
        # Save to disk
        episode_path = self.storage_dir / f"{self.current_episode.episode_id}.json"
        with open(episode_path, 'w') as f:
            json.dump(self.current_episode.to_dict(), f, indent=2)
        
        summary = self.current_episode.get_summary()
        self.current_episode = None
        
        return summary
        
    def load_episode(self, episode_id: str) -> Dict:
        """Load an episode from disk"""
        episode_path = self.storage_dir / f"{episode_id}.json"
        
        if not episode_path.exists():
            raise FileNotFoundError(f"Episode {episode_id} not found")
        
        with open(episode_path, 'r') as f:
            return json.load(f)
            
    def list_episodes(self) -> List[Dict]:
        """List all stored episodes"""
        episodes = []
        
        for episode_file in self.storage_dir.glob("*.json"):
            try:
                with open(episode_file, 'r') as f:
                    data = json.load(f)
                    episodes.append({
                        "episode_id": data["episode_id"],
                        "metadata": data.get("metadata", {}),
                        "start_time": data["start_time"],
                        "end_time": data.get("end_time"),
                        "num_frames": data.get("num_frames", 0)
                    })
            except Exception as e:
                print(f"Error loading episode {episode_file}: {e}")
                continue
        
        # Sort by start time (newest first)
        episodes.sort(key=lambda x: x["start_time"], reverse=True)
        return episodes
        
    def delete_episode(self, episode_id: str):
        """Delete an episode"""
        episode_path = self.storage_dir / f"{episode_id}.json"
        if episode_path.exists():
            episode_path.unlink()
        
    def get_episode_frames(self, episode_id: str, 
                          start_frame: int = 0, 
                          end_frame: int = None) -> List[Dict]:
        """Get specific frames from an episode"""
        episode_data = self.load_episode(episode_id)
        frames = episode_data.get("frames", [])
        
        if end_frame is None:
            end_frame = len(frames)
        
        return frames[start_frame:end_frame]


# Global logger instance
episode_logger = EpisodeLogger()
