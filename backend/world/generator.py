"""
World generation models and logic
Generates 3D scenes from text prompts
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import random
import math


class Object3D(BaseModel):
    """3D object in the scene"""
    id: str
    type: str  # cube, sphere, plane, character, prop
    position: List[float] = Field(default_factory=lambda: [0, 0, 0])
    rotation: List[float] = Field(default_factory=lambda: [0, 0, 0])
    scale: List[float] = Field(default_factory=lambda: [1, 1, 1])
    color: str = "#888888"
    name: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class WorldScene(BaseModel):
    """Complete world scene"""
    id: str
    name: str
    description: str
    objects: List[Object3D]
    lighting: Dict[str, Any] = Field(default_factory=dict)
    physics_config: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorldGenerator:
    """Generates 3D worlds from text prompts"""
    
    def __init__(self):
        self.object_id_counter = 0
        
    def _generate_id(self) -> str:
        """Generate unique object ID"""
        self.object_id_counter += 1
        return f"obj_{self.object_id_counter}"
    
    def generate_from_prompt(self, prompt: str) -> WorldScene:
        """
        Generate a world scene from a text prompt
        This is a simplified version - in production, you'd use an AI model
        """
        prompt_lower = prompt.lower()
        objects = []
        
        # Ground plane
        objects.append(Object3D(
            id=self._generate_id(),
            type="plane",
            name="ground",
            position=[0, 0, 0],
            scale=[20, 1, 20],
            color="#4a7c59",
            properties={"isStatic": True}
        ))
        
        # Parse prompt for common keywords and generate appropriate objects
        if "room" in prompt_lower or "indoor" in prompt_lower:
            objects.extend(self._generate_room())
        elif "outdoor" in prompt_lower or "park" in prompt_lower:
            objects.extend(self._generate_outdoor())
        elif "stage" in prompt_lower or "theater" in prompt_lower:
            objects.extend(self._generate_stage())
        else:
            # Default: simple scene with some objects
            objects.extend(self._generate_default_scene())
        
        # Add some decorative elements based on keywords
        if "tree" in prompt_lower:
            objects.extend(self._add_trees(count=random.randint(2, 5)))
        
        if "building" in prompt_lower or "house" in prompt_lower:
            objects.extend(self._add_buildings(count=random.randint(1, 3)))
        
        # Lighting configuration
        lighting = {
            "ambient": {"color": "#ffffff", "intensity": 0.5},
            "directional": {
                "color": "#ffffff",
                "intensity": 1.0,
                "position": [10, 10, 5]
            }
        }
        
        # Physics configuration
        physics_config = {
            "gravity": [0, -9.81, 0],
            "enabled": True
        }
        
        return WorldScene(
            id=f"world_{random.randint(1000, 9999)}",
            name=f"Generated Scene",
            description=prompt,
            objects=objects,
            lighting=lighting,
            physics_config=physics_config,
            metadata={"prompt": prompt, "generated_at": "now"}
        )
    
    def _generate_room(self) -> List[Object3D]:
        """Generate indoor room"""
        objects = []
        
        # Walls
        wall_height = 3
        room_size = 10
        
        # Back wall
        objects.append(Object3D(
            id=self._generate_id(),
            type="cube",
            name="wall_back",
            position=[0, wall_height/2, -room_size/2],
            scale=[room_size, wall_height, 0.2],
            color="#d4c4a8",
            properties={"isStatic": True}
        ))
        
        # Side walls
        objects.append(Object3D(
            id=self._generate_id(),
            type="cube",
            name="wall_left",
            position=[-room_size/2, wall_height/2, 0],
            scale=[0.2, wall_height, room_size],
            color="#d4c4a8",
            properties={"isStatic": True}
        ))
        
        objects.append(Object3D(
            id=self._generate_id(),
            type="cube",
            name="wall_right",
            position=[room_size/2, wall_height/2, 0],
            scale=[0.2, wall_height, room_size],
            color="#d4c4a8",
            properties={"isStatic": True}
        ))
        
        # Furniture
        objects.append(Object3D(
            id=self._generate_id(),
            type="cube",
            name="table",
            position=[0, 0.4, 0],
            scale=[2, 0.1, 1],
            color="#8b4513",
            properties={"isStatic": True}
        ))
        
        return objects
    
    def _generate_outdoor(self) -> List[Object3D]:
        """Generate outdoor scene"""
        objects = []
        
        # Add some terrain variation
        for i in range(5):
            x = random.uniform(-8, 8)
            z = random.uniform(-8, 8)
            objects.append(Object3D(
                id=self._generate_id(),
                type="sphere",
                name=f"rock_{i}",
                position=[x, 0.3, z],
                scale=[0.6, 0.6, 0.6],
                color="#808080",
                properties={"isStatic": True}
            ))
        
        return objects
    
    def _generate_stage(self) -> List[Object3D]:
        """Generate theater stage"""
        objects = []
        
        # Stage platform
        objects.append(Object3D(
            id=self._generate_id(),
            type="cube",
            name="stage",
            position=[0, 0.5, -2],
            scale=[8, 1, 4],
            color="#654321",
            properties={"isStatic": True}
        ))
        
        # Backdrop
        objects.append(Object3D(
            id=self._generate_id(),
            type="cube",
            name="backdrop",
            position=[0, 2, -4],
            scale=[8, 4, 0.2],
            color="#1a1a2e",
            properties={"isStatic": True}
        ))
        
        return objects
    
    def _generate_default_scene(self) -> List[Object3D]:
        """Generate default scene with basic objects"""
        objects = []
        
        # Add some cubes and spheres
        for i in range(3):
            angle = (i / 3) * 2 * math.pi
            radius = 3
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            obj_type = "cube" if i % 2 == 0 else "sphere"
            objects.append(Object3D(
                id=self._generate_id(),
                type=obj_type,
                name=f"object_{i}",
                position=[x, 0.5, z],
                scale=[1, 1, 1],
                color=random.choice(["#ff6b6b", "#4ecdc4", "#45b7d1", "#f7d794"]),
                properties={"isStatic": False}
            ))
        
        return objects
    
    def _add_trees(self, count: int) -> List[Object3D]:
        """Add trees to scene"""
        objects = []
        for i in range(count):
            x = random.uniform(-7, 7)
            z = random.uniform(-7, 7)
            
            # Trunk
            objects.append(Object3D(
                id=self._generate_id(),
                type="cube",
                name=f"tree_trunk_{i}",
                position=[x, 1, z],
                scale=[0.3, 2, 0.3],
                color="#8b4513",
                properties={"isStatic": True}
            ))
            
            # Foliage
            objects.append(Object3D(
                id=self._generate_id(),
                type="sphere",
                name=f"tree_foliage_{i}",
                position=[x, 2.5, z],
                scale=[1.5, 1.5, 1.5],
                color="#228b22",
                properties={"isStatic": True}
            ))
        
        return objects
    
    def _add_buildings(self, count: int) -> List[Object3D]:
        """Add buildings to scene"""
        objects = []
        for i in range(count):
            x = random.uniform(-8, 8)
            z = random.uniform(-8, 8)
            height = random.uniform(2, 5)
            
            objects.append(Object3D(
                id=self._generate_id(),
                type="cube",
                name=f"building_{i}",
                position=[x, height/2, z],
                scale=[2, height, 2],
                color=random.choice(["#bdc3c7", "#95a5a6", "#7f8c8d"]),
                properties={"isStatic": True}
            ))
        
        return objects


# Global generator instance
world_generator = WorldGenerator()
