"""
Physics simulation using Pymunk
Provides 2D physics that can be visualized in 3D
"""
import pymunk
from typing import Dict, List, Tuple, Optional
import math


class PhysicsEngine:
    """Simple physics engine for the drama world"""
    
    def __init__(self, gravity: Tuple[float, float] = (0, -9.81)):
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.bodies: Dict[str, pymunk.Body] = {}
        self.shapes: Dict[str, pymunk.Shape] = {}
        
    def add_static_body(self, object_id: str, position: Tuple[float, float], 
                       shape_type: str = "box", size: Tuple[float, float] = (1, 1)):
        """Add a static (non-moving) body"""
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = position
        
        if shape_type == "box":
            shape = pymunk.Poly.create_box(body, size)
        else:  # circle
            shape = pymunk.Circle(body, size[0])
        
        shape.friction = 0.7
        self.space.add(body, shape)
        
        self.bodies[object_id] = body
        self.shapes[object_id] = shape
        
    def add_dynamic_body(self, object_id: str, position: Tuple[float, float],
                        mass: float = 1.0, shape_type: str = "box", 
                        size: Tuple[float, float] = (1, 1)):
        """Add a dynamic (physics-simulated) body"""
        if shape_type == "box":
            moment = pymunk.moment_for_box(mass, size)
        else:  # circle
            moment = pymunk.moment_for_circle(mass, 0, size[0])
        
        body = pymunk.Body(mass, moment)
        body.position = position
        
        if shape_type == "box":
            shape = pymunk.Poly.create_box(body, size)
        else:  # circle
            shape = pymunk.Circle(body, size[0])
        
        shape.friction = 0.7
        shape.elasticity = 0.5
        
        self.space.add(body, shape)
        self.bodies[object_id] = body
        self.shapes[object_id] = shape
        
    def apply_force(self, object_id: str, force: Tuple[float, float]):
        """Apply force to a body"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            body.apply_force_at_local_point(force, (0, 0))
    
    def set_velocity(self, object_id: str, velocity: Tuple[float, float]):
        """Set velocity of a body"""
        if object_id in self.bodies:
            self.bodies[object_id].velocity = velocity
    
    def get_position(self, object_id: str) -> Optional[Tuple[float, float]]:
        """Get position of a body"""
        if object_id in self.bodies:
            pos = self.bodies[object_id].position
            return (pos.x, pos.y)
        return None
    
    def get_velocity(self, object_id: str) -> Optional[Tuple[float, float]]:
        """Get velocity of a body"""
        if object_id in self.bodies:
            vel = self.bodies[object_id].velocity
            return (vel.x, vel.y)
        return None
    
    def get_angle(self, object_id: str) -> Optional[float]:
        """Get rotation angle of a body"""
        if object_id in self.bodies:
            return self.bodies[object_id].angle
        return None
    
    def step(self, dt: float = 1.0/60.0):
        """Advance physics simulation by dt seconds"""
        self.space.step(dt)
    
    def remove_body(self, object_id: str):
        """Remove a body from the simulation"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            shape = self.shapes[object_id]
            self.space.remove(body, shape)
            del self.bodies[object_id]
            del self.shapes[object_id]
    
    def get_all_states(self) -> Dict[str, Dict]:
        """Get state of all bodies"""
        states = {}
        for object_id, body in self.bodies.items():
            states[object_id] = {
                "position": (body.position.x, body.position.y),
                "velocity": (body.velocity.x, body.velocity.y),
                "angle": body.angle,
                "angular_velocity": body.angular_velocity
            }
        return states
    
    def reset(self):
        """Reset the physics simulation"""
        for body in list(self.bodies.values()):
            for shape in body.shapes:
                self.space.remove(shape)
            self.space.remove(body)
        self.bodies.clear()
        self.shapes.clear()
