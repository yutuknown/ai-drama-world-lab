# AI Drama World Lab 🎭

An innovative AI-powered platform for creating interactive 3D anime/drama worlds with emergent AI agents. Generate dynamic scenes from text prompts, spawn intelligent agents with goals and memory, and watch emergent narratives unfold in real-time.

![AI Drama World Lab](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

### 🌍 World Generation
- **Text-to-3D Scene Generation**: Create 3D environments from natural language descriptions
- **Multiple Scene Templates**: Indoor rooms, outdoor parks, theater stages, and more
- **Dynamic Object Placement**: Procedurally generated props, buildings, and decorations
- **Real-time Physics**: Integrated physics simulation using Pymunk

### 🤖 Embodied AI Agents
- **Goal-Oriented Behavior**: Agents pursue specified goals autonomously
- **PPO Reinforcement Learning**: Agents learn from experience using Proximal Policy Optimization
- **Memory System**: Short-term, long-term, and episodic memory for contextual decision-making
- **Emotional States**: Agents exhibit emotional responses (happy, frustrated, neutral)
- **Energy Management**: Agents must manage energy levels and rest when needed

### 🎬 Episode Recording & Replay
- **Complete Session Recording**: Capture entire simulation sessions frame-by-frame
- **Playback Controls**: Review episodes with play/pause/scrub functionality
- **Episode Management**: List, view, and delete recorded episodes
- **Frame-by-Frame Analysis**: Inspect agent states and world data at any point

### 🎨 User Interfaces
1. **Scene Designer**: Generate and customize 3D worlds
2. **Agent Studio**: Create and manage AI agents
3. **Episode Viewer**: Review and replay recorded simulations
4. **Simulation Controller**: Start/stop simulations and adjust parameters

### 🚀 Technical Stack
- **Frontend**: Next.js 14, React, TypeScript, Three.js, React Three Fiber
- **Backend**: FastAPI, Python, PyTorch, Stable-Baselines3
- **Physics**: Pymunk 2D physics engine
- **3D Rendering**: Three.js with WebGL
- **State Management**: Zustand
- **Real-time Communication**: WebSockets

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)

### Docker Installation (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yutuknown/ai-drama-world-lab.git
cd ai-drama-world-lab
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open http://localhost:3000 in your browser

## Usage Guide

### 1. Creating a World

1. Navigate to the **Scene Designer** tab
2. Enter a text description of your desired scene:
   - "A cozy indoor room with furniture"
   - "An outdoor park with trees"
   - "A theater stage with backdrop"
3. Click "Generate Scene"
4. View your generated 3D world in the viewport

### 2. Creating Agents

1. Navigate to the **Agent Studio** tab
2. Fill in the agent details:
   - **Name**: Give your agent a name
   - **Goal**: Specify what the agent should try to achieve
   - **Personality**: Choose from neutral, curious, cautious, or bold
3. Click "Create Agent"
4. The agent will appear in the 3D scene

### 3. Running a Simulation

1. Create at least one scene and one agent
2. Use the **Simulation Controller** at the bottom
3. Click "Start Simulation"
4. Watch agents interact with the world in real-time
5. Click "Stop Simulation" to end and save the episode

### 4. Viewing Episodes

1. Navigate to the **Episode Viewer** tab
2. Browse recorded episodes
3. Click "View" on any episode to replay it
4. Use playback controls to review the simulation

## API Documentation

### World Generation

**POST** `/api/world/generate`
```json
{
  "prompt": "A cozy indoor room with furniture"
}
```

**GET** `/api/world/templates`

### Agent Management

**POST** `/api/agents/create`
```json
{
  "name": "Agent Alpha",
  "goal": "Explore the world",
  "personality": "curious"
}
```

**GET** `/api/agents/list`

**POST** `/api/agents/{agent_id}/step`

**POST** `/api/agents/{agent_id}/train`

**DELETE** `/api/agents/{agent_id}`

### Episode Recording

**POST** `/api/episodes/start`
```json
{
  "name": "My Simulation",
  "description": "Testing agent behavior"
}
```

**POST** `/api/episodes/log`

**POST** `/api/episodes/end`

**GET** `/api/episodes/list`

**GET** `/api/episodes/{episode_id}`

**DELETE** `/api/episodes/{episode_id}`

Full API documentation available at: http://localhost:8000/docs

## Architecture

```
ai-drama-world-lab/
├── backend/
│   ├── agents/              # AI agent implementation
│   │   ├── embodied_agent.py    # Base agent class with memory
│   │   └── ppo_trainer.py       # PPO learning algorithm
│   ├── world/               # World generation
│   │   ├── generator.py         # Scene generation from text
│   │   └── physics.py           # Physics simulation
│   ├── api/                 # REST API endpoints
│   │   ├── world.py
│   │   ├── agents.py
│   │   └── episodes.py
│   ├── utils/               # Utilities
│   │   ├── episode_logger.py    # Episode recording
│   │   └── websocket_manager.py # Real-time updates
│   ├── main.py              # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js app router
│   │   ├── components/      # React components
│   │   │   ├── Scene3D.tsx          # Three.js scene
│   │   │   ├── SceneDesigner.tsx    # World creation UI
│   │   │   ├── AgentStudio.tsx      # Agent management UI
│   │   │   ├── EpisodeViewer.tsx    # Episode playback UI
│   │   │   └── SimulationController.tsx
│   │   ├── lib/             # API client
│   │   ├── store/           # State management
│   │   └── types/           # TypeScript types
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Key Components

### Backend

#### Embodied Agent
- Perception: Observes world state within radius
- Decision: Uses PPO policy or heuristics
- Action: Moves, interacts, or rests
- Learning: Updates policy based on rewards
- Memory: Stores experiences for learning

#### World Generator
- Parses text prompts
- Generates 3D objects procedurally
- Configures lighting and physics
- Supports multiple scene types

#### Episode Logger
- Records frame-by-frame simulation data
- Stores agent states and world states
- Enables replay and analysis
- JSON-based storage format

### Frontend

#### Scene3D Component
- Three.js WebGL rendering
- Real-time object updates
- Camera controls (orbit)
- Lighting and shadows
- Agent visualization

#### UI Components
- **SceneDesigner**: Text-to-3D generation interface
- **AgentStudio**: Agent creation and management
- **EpisodeViewer**: Episode playback with controls
- **SimulationController**: Simulation control panel

## Configuration

### Environment Variables

#### Backend
```bash
# No environment variables required for basic setup
```

#### Frontend
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker Compose

Modify `docker-compose.yml` to change:
- Port mappings
- Volume mounts
- Resource limits

## Development

### Adding New Scene Types

Edit `backend/world/generator.py`:

```python
def _generate_custom_scene(self) -> List[Object3D]:
    # Add your scene generation logic
    pass
```

### Customizing Agent Behavior

Edit `backend/agents/embodied_agent.py`:

```python
def decide_action(self, observation: np.ndarray) -> Dict[str, Any]:
    # Customize decision-making logic
    pass
```

### Adding New UI Components

Create a new component in `frontend/src/components/`:

```tsx
export default function MyComponent() {
  return <div>My Component</div>;
}
```

## Performance Optimization

- Adjust simulation FPS in the UI (1-60 FPS)
- Limit number of agents for better performance
- Reduce observation radius for faster perception
- Use lower polygon models for objects

## Troubleshooting

### Issue: Backend fails to start
- Check Python version (3.10+ required)
- Ensure all dependencies are installed
- Check port 8000 is not in use

### Issue: Frontend fails to build
- Check Node.js version (18+ required)
- Clear node_modules and reinstall
- Check for TypeScript errors

### Issue: 3D scene not rendering
- Check browser WebGL support
- Disable ad blockers
- Try a different browser (Chrome recommended)

### Issue: Agents not moving
- Ensure a scene is created first
- Check that simulation is running
- Verify agents have energy

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Future Enhancements

- [ ] Multi-agent communication protocols
- [ ] Advanced NLP for scene understanding
- [ ] More sophisticated learning algorithms (SAC, TD3)
- [ ] 3D model import support
- [ ] Voice-based agent interaction
- [ ] Persistent agent memory across episodes
- [ ] Collaborative multi-user sessions
- [ ] Advanced physics (ragdoll, cloth simulation)
- [ ] Export episodes as video

## Acknowledgments

- Three.js for 3D rendering
- FastAPI for the backend framework
- Stable-Baselines3 for RL algorithms
- React Three Fiber for React integration
- Pymunk for 2D physics

---

Made with ❤️ by the AI Drama World Lab team
