"""
Episode logging and replay API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from utils.episode_logger import episode_logger

router = APIRouter()


class StartEpisodeRequest(BaseModel):
    """Request to start episode recording"""
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@router.post("/start")
async def start_episode(request: StartEpisodeRequest):
    """Start recording a new episode"""
    try:
        metadata = request.metadata or {}
        if request.name:
            metadata["name"] = request.name
        if request.description:
            metadata["description"] = request.description
        
        episode_id = episode_logger.start_episode(metadata)
        return {
            "episode_id": episode_id,
            "message": "Episode recording started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting episode: {str(e)}")


@router.post("/log")
async def log_frame(
    timestamp: float,
    agents_state: List[Dict],
    world_state: Dict,
    events: Optional[List[Dict]] = None
):
    """Log a frame to the current episode"""
    try:
        episode_logger.log_frame(timestamp, agents_state, world_state, events)
        return {"message": "Frame logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging frame: {str(e)}")


@router.post("/end")
async def end_episode():
    """End current episode recording"""
    try:
        summary = episode_logger.end_episode()
        return {
            "message": "Episode recording ended",
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ending episode: {str(e)}")


@router.get("/list")
async def list_episodes():
    """List all recorded episodes"""
    try:
        episodes = episode_logger.list_episodes()
        return {"episodes": episodes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing episodes: {str(e)}")


@router.get("/{episode_id}")
async def get_episode(episode_id: str):
    """Get full episode data"""
    try:
        episode_data = episode_logger.load_episode(episode_id)
        return episode_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Episode not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading episode: {str(e)}")


@router.get("/{episode_id}/frames")
async def get_episode_frames(
    episode_id: str,
    start: int = 0,
    end: Optional[int] = None
):
    """Get specific frames from an episode"""
    try:
        frames = episode_logger.get_episode_frames(episode_id, start, end)
        return {"frames": frames, "count": len(frames)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Episode not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading frames: {str(e)}")


@router.delete("/{episode_id}")
async def delete_episode(episode_id: str):
    """Delete an episode"""
    try:
        episode_logger.delete_episode(episode_id)
        return {"message": "Episode deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting episode: {str(e)}")
