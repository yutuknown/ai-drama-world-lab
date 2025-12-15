# Usage Examples

This document provides code examples for common use cases.

## Python API Client

### Basic World Generation

```python
import requests

API_URL = "http://localhost:8000"

# Generate a scene
response = requests.post(f"{API_URL}/api/world/generate", json={
    "prompt": "A cozy indoor room with furniture"
})
scene = response.json()
print(f"Generated scene: {scene['name']}")
print(f"Number of objects: {len(scene['objects'])}")
```

### Creating and Managing Agents

```python
import requests
import time

API_URL = "http://localhost:8000"

# Create an agent
response = requests.post(f"{API_URL}/api/agents/create", json={
    "name": "Explorer",
    "goal": "Find and interact with all objects",
    "personality": "curious"
})
agent = response.json()
agent_id = agent['id']
print(f"Created agent: {agent['name']} (ID: {agent_id})")

# Get agent state
response = requests.get(f"{API_URL}/api/agents/{agent_id}")
state = response.json()
print(f"Agent energy: {state['energy']}")
print(f"Agent emotion: {state['emotional_state']}")

# Step the agent
world_state = {"objects": [], "agents": [agent]}
response = requests.post(f"{API_URL}/api/agents/{agent_id}/step", json=world_state)
result = response.json()
print(f"Agent action: {result['action']['name']}")
print(f"Reward: {result['reward']}")

# Train the agent
response = requests.post(f"{API_URL}/api/agents/{agent_id}/train")
metrics = response.json()
print(f"Training metrics: {metrics['metrics']}")
```

### Recording Episodes

```python
import requests
import time

API_URL = "http://localhost:8000"

# Start episode recording
response = requests.post(f"{API_URL}/api/episodes/start", json={
    "name": "My First Episode",
    "description": "Testing episode recording"
})
episode_id = response.json()['episode_id']
print(f"Started episode: {episode_id}")

# Simulate for 10 frames
for i in range(10):
    # Log frame
    requests.post(f"{API_URL}/api/episodes/log", json={
        "timestamp": i * 0.1,
        "agents_state": [],
        "world_state": {},
        "events": []
    })
    time.sleep(0.1)

# End episode
response = requests.post(f"{API_URL}/api/episodes/end")
summary = response.json()['summary']
print(f"Episode ended. Frames recorded: {summary['num_frames']}")

# List all episodes
response = requests.get(f"{API_URL}/api/episodes/list")
episodes = response.json()['episodes']
print(f"Total episodes: {len(episodes)}")

# Get episode details
response = requests.get(f"{API_URL}/api/episodes/{episode_id}")
episode = response.json()
print(f"Episode duration: {episode.get('end_time', 'N/A')}")
```

## JavaScript/TypeScript Frontend

### Generating a Scene

```typescript
import { worldAPI } from '@/lib/api';

async function generateScene() {
  try {
    const scene = await worldAPI.generate("A peaceful garden with trees");
    console.log('Generated scene:', scene.name);
    console.log('Objects:', scene.objects.length);
    return scene;
  } catch (error) {
    console.error('Failed to generate scene:', error);
  }
}
```

### Creating Agents

```typescript
import { agentAPI } from '@/lib/api';

async function createAgent() {
  try {
    const agent = await agentAPI.create(
      "Agent Alpha",
      "Explore and learn",
      "curious",
      [0, 0.5, 0]
    );
    console.log('Created agent:', agent.name);
    return agent;
  } catch (error) {
    console.error('Failed to create agent:', error);
  }
}
```

### Running a Simulation Loop

```typescript
import { agentAPI, episodeAPI } from '@/lib/api';

async function runSimulation(agents: any[], scene: any, duration: number) {
  // Start episode
  const { episode_id } = await episodeAPI.start(
    "Simulation Run",
    "Automated simulation"
  );
  
  const fps = 10;
  const frameTime = 1 / fps;
  let currentTime = 0;
  
  // Simulation loop
  const intervalId = setInterval(async () => {
    if (currentTime >= duration) {
      clearInterval(intervalId);
      await episodeAPI.end();
      console.log('Simulation complete');
      return;
    }
    
    // Step all agents
    const worldState = { objects: scene.objects, agents };
    
    for (const agent of agents) {
      const result = await agentAPI.step(agent.id, worldState);
      
      // Update agent state
      Object.assign(agent, result.agent_state);
    }
    
    // Log frame
    await episodeAPI.logFrame(currentTime, agents, worldState);
    
    currentTime += frameTime;
  }, frameTime * 1000);
}
```

### React Component Integration

```tsx
'use client';

import { useState, useEffect } from 'react';
import { worldAPI, agentAPI } from '@/lib/api';
import { useAppStore } from '@/store/appStore';

export default function QuickStartExample() {
  const { setScene, addAgent } = useAppStore();
  const [loading, setLoading] = useState(false);
  
  const handleQuickStart = async () => {
    setLoading(true);
    
    try {
      // 1. Generate scene
      const scene = await worldAPI.generate("A simple room");
      setScene(scene);
      
      // 2. Create agent
      const agent = await agentAPI.create(
        "Test Agent",
        "Explore the room",
        "curious"
      );
      addAgent(agent);
      
      console.log('Setup complete!');
    } catch (error) {
      console.error('Setup failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <button onClick={handleQuickStart} disabled={loading}>
      {loading ? 'Setting up...' : 'Quick Start'}
    </button>
  );
}
```

## WebSocket Usage

### Python WebSocket Client

```python
import asyncio
import websockets
import json

async def listen_to_updates():
    uri = "ws://localhost:8000/ws"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received: {data}")

# Run the client
asyncio.run(listen_to_updates())
```

### JavaScript WebSocket Client

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('WebSocket connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket disconnected');
};
```

## Batch Operations

### Create Multiple Agents

```python
import requests

API_URL = "http://localhost:8000"

agents = []
personalities = ["curious", "cautious", "bold"]

for i, personality in enumerate(personalities):
    response = requests.post(f"{API_URL}/api/agents/create", json={
        "name": f"Agent {i+1}",
        "goal": "Explore the world",
        "personality": personality,
        "position": [i * 2, 0.5, 0]
    })
    agents.append(response.json())

print(f"Created {len(agents)} agents")
```

### Parallel Agent Steps

```python
import requests
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8000"

def step_agent(agent_id, world_state):
    response = requests.post(
        f"{API_URL}/api/agents/{agent_id}/step",
        json=world_state
    )
    return response.json()

# Step all agents in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(
        lambda aid: step_agent(aid, world_state),
        agent_ids
    ))
```

## Advanced Scenarios

### Custom Scene Generation

```python
import requests

# Generate a complex scene
response = requests.post(f"{API_URL}/api/world/generate", json={
    "prompt": "A bustling outdoor marketplace with stalls, trees, and buildings"
})
scene = response.json()

# Analyze the scene
print(f"Scene contains {len(scene['objects'])} objects:")
for obj in scene['objects']:
    print(f"  - {obj['name']}: {obj['type']} at {obj['position']}")
```

### Agent Learning Over Time

```python
import requests
import time

API_URL = "http://localhost:8000"

# Create agent
response = requests.post(f"{API_URL}/api/agents/create", json={
    "name": "Learner",
    "goal": "Maximize rewards",
    "personality": "curious"
})
agent_id = response.json()['id']

# Train over multiple episodes
for episode in range(10):
    print(f"\nEpisode {episode + 1}")
    
    # Collect 100 experiences
    for step in range(100):
        response = requests.post(
            f"{API_URL}/api/agents/{agent_id}/step",
            json={"objects": [], "agents": []}
        )
        result = response.json()
    
    # Train
    response = requests.post(f"{API_URL}/api/agents/{agent_id}/train")
    metrics = response.json()['metrics']
    print(f"  Loss: {metrics['loss']:.4f}")
    print(f"  Mean Return: {metrics['mean_return']:.4f}")
```

## Error Handling

### Robust API Calls

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"API call failed: {e}")
        return None

# Usage
scene = safe_api_call('POST', f"{API_URL}/api/world/generate", 
                     json={"prompt": "A room"})
if scene:
    print(f"Generated: {scene['name']}")
else:
    print("Failed to generate scene")
```

## Testing

### Unit Test Example

```python
import unittest
import requests

class TestWorldAPI(unittest.TestCase):
    API_URL = "http://localhost:8000"
    
    def test_generate_scene(self):
        response = requests.post(f"{self.API_URL}/api/world/generate", json={
            "prompt": "Test scene"
        })
        self.assertEqual(response.status_code, 200)
        scene = response.json()
        self.assertIn('id', scene)
        self.assertIn('objects', scene)
        self.assertGreater(len(scene['objects']), 0)
    
    def test_list_templates(self):
        response = requests.get(f"{self.API_URL}/api/world/templates")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('templates', data)
        self.assertGreater(len(data['templates']), 0)

if __name__ == '__main__':
    unittest.main()
```
