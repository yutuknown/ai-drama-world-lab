# Architecture Overview

## System Architecture

AI Drama World Lab follows a client-server architecture with clear separation between frontend and backend components.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Scene      │  │    Agent     │  │   Episode    │    │
│  │   Designer   │  │    Studio    │  │   Viewer     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           Three.js 3D Scene Renderer                │  │
│  │         (WebGL, Camera, Lighting, Objects)          │  │
│  └─────────────────────────────────────────────────────┘  │
│                          ↕                                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │    API Client (Axios) + WebSocket Manager           │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↕ HTTP/WS
┌─────────────────────────────────────────────────────────────┐
│                         Backend                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              FastAPI REST API                        │  │
│  │    /world   /agents   /episodes   WebSocket         │  │
│  └─────────────────────────────────────────────────────┘  │
│                          ↓                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐  │
│  │   World    │  │   Agent    │  │     Episode        │  │
│  │ Generator  │  │  System    │  │     Logger         │  │
│  │            │  │            │  │                    │  │
│  │ • Parser   │  │ • Embodied │  │ • Recording       │  │
│  │ • Builder  │  │ • PPO      │  │ • Playback        │  │
│  │ • Physics  │  │ • Memory   │  │ • Storage         │  │
│  └────────────┘  └────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Component Hierarchy

```
App (page.tsx)
├── Header
├── Viewport
│   └── Scene3D (Three.js)
│       ├── Camera + Controls
│       ├── Lighting
│       ├── SceneObject3D (for each world object)
│       └── AgentMesh (for each agent)
└── Sidebar
    ├── Tabs
    ├── TabContent
    │   ├── SceneDesigner
    │   ├── AgentStudio
    │   └── EpisodeViewer
    └── SimulationController
```

### State Management

Uses Zustand for global state:
- `currentScene`: Active 3D scene
- `agents`: List of active agents
- `isSimulating`: Simulation status
- `currentEpisodeId`: Active recording session

### API Communication

- **REST API**: Axios for CRUD operations
- **WebSocket**: Real-time updates during simulation
- **API Client**: Centralized in `lib/api.ts`

## Backend Architecture

### Core Modules

#### 1. World Generation (`world/`)
- **generator.py**: Scene generation from text prompts
- **physics.py**: Physics simulation using Pymunk

#### 2. Agent System (`agents/`)
- **embodied_agent.py**: Agent with perception, action, memory
- **ppo_trainer.py**: PPO reinforcement learning

#### 3. API Layer (`api/`)
- **world.py**: World generation endpoints
- **agents.py**: Agent management endpoints
- **episodes.py**: Episode recording endpoints

#### 4. Utilities (`utils/`)
- **episode_logger.py**: Frame-by-frame recording
- **websocket_manager.py**: Real-time communication

### Data Flow

#### Simulation Loop

```
1. User starts simulation
   ↓
2. Backend: Start episode recording
   ↓
3. For each frame:
   a. Frontend requests agent step
   b. Agent perceives world state
   c. Agent decides action (via PPO)
   d. Agent executes action
   e. Calculate reward
   f. Update agent state
   g. Log frame to episode
   h. Send state to frontend
   i. Frontend updates 3D scene
   ↓
4. User stops simulation
   ↓
5. Backend: Save episode to disk
```

#### World Generation

```
1. User enters prompt
   ↓
2. Frontend sends to /world/generate
   ↓
3. Backend parses prompt
   ↓
4. Generate objects based on keywords
   ↓
5. Configure lighting and physics
   ↓
6. Return WorldScene JSON
   ↓
7. Frontend renders in Three.js
```

#### Agent Learning

```
1. Agent collects experiences
   ↓
2. Store in PPO buffer:
   - Observation
   - Action
   - Reward
   - Value estimate
   ↓
3. When buffer fills:
   a. Compute returns
   b. Calculate advantages
   c. Update policy network
   d. Update value network
   ↓
4. Clear buffer
```

## Technology Stack Details

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Three.js**: 3D graphics library
- **React Three Fiber**: React renderer for Three.js
- **@react-three/drei**: Helper components
- **Zustand**: State management
- **Axios**: HTTP client

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **PyTorch**: Deep learning framework
- **Gymnasium**: RL environment interface
- **Stable-Baselines3**: RL algorithms
- **Pymunk**: 2D physics engine
- **WebSockets**: Real-time communication

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Design Patterns

### Backend Patterns
- **Router Pattern**: Separate routers for different domains
- **Manager Pattern**: Global managers (WebSocket, Episode Logger)
- **Factory Pattern**: Object generation in world generator
- **Observer Pattern**: WebSocket broadcasts

### Frontend Patterns
- **Container/Presentation**: Separating logic and UI
- **Custom Hooks**: Reusable state logic
- **Composition**: Building complex UIs from simple components
- **Context-free State**: Using Zustand instead of React Context

## Scalability Considerations

### Current Implementation
- Single-threaded simulation
- In-memory agent storage
- File-based episode storage
- No authentication/authorization

### Production Enhancements
- Multi-process simulation with Ray
- Database for agents (PostgreSQL/MongoDB)
- Object storage for episodes (S3)
- Redis for caching and pub/sub
- Authentication with JWT
- Rate limiting
- Load balancing
- Horizontal scaling

## Security Considerations

### Current Status
- No authentication
- No input sanitization beyond Pydantic
- CORS enabled for localhost only
- No rate limiting

### Production Recommendations
- Add API authentication (JWT/OAuth)
- Implement rate limiting
- Input validation and sanitization
- HTTPS/WSS for encrypted communication
- Security headers (CORS, CSP)
- SQL injection prevention (not applicable - no SQL)
- XSS prevention in frontend

## Performance Considerations

### Optimization Strategies
- Limit simulation FPS
- Batch API calls where possible
- Use WebSocket for frequent updates
- Implement pagination for episodes
- Lazy load 3D models
- Use instancing for repeated objects
- Optimize Three.js scene graph

### Monitoring Points
- API response times
- WebSocket message rate
- Frontend FPS
- Memory usage (agents, episode data)
- Episode storage size
