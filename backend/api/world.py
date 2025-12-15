"""
World generation API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from world.generator import world_generator, WorldScene

router = APIRouter()


class GenerateWorldRequest(BaseModel):
    """Request to generate a world"""
    prompt: str
    seed: Optional[int] = None


@router.post("/generate", response_model=WorldScene)
async def generate_world(request: GenerateWorldRequest):
    """
    Generate a 3D world from a text prompt
    
    Example prompts:
    - "A cozy indoor room with furniture"
    - "An outdoor park with trees"
    - "A theater stage with backdrop"
    """
    try:
        scene = world_generator.generate_from_prompt(request.prompt)
        return scene
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating world: {str(e)}")


@router.get("/templates")
async def list_templates():
    """List available world templates"""
    return {
        "templates": [
            {"id": "room", "name": "Indoor Room", "description": "A cozy indoor room"},
            {"id": "outdoor", "name": "Outdoor Scene", "description": "An outdoor environment"},
            {"id": "stage", "name": "Theater Stage", "description": "A performance stage"},
            {"id": "default", "name": "Default Scene", "description": "A simple scene with objects"}
        ]
    }
