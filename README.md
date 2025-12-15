# ai-drama-world-lab
An innovative AI-powered platform for creating interactive 3D anime/drama worlds with emergent AI agents. Generate dynamic scenes from text prompts, spawn intelligent agents with goals and memory, and watch emergent narratives unfold in real-time. Features world generation, agent learning, story logging, and episode replay.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Key Components](#key-components)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)

## Overview

**AI Drama World Lab** is an innovative platform that combines cutting-edge AI technologies to create interactive 3D worlds populated with intelligent agents. Think of it as a generative AI playground for anime/drama storytelling where:

1. **Text-to-World Generation**: Convert detailed text prompts into dynamic 3D environments
2. **Embodied AI Agents**: Spawn intelligent characters with neural policies, long-term memory, and emergent behaviors
3. **Emergent Narratives**: Watch unscripted stories unfold as agents interact based on their goals
4. **Real-time Physics**: Full physics simulation at 60 FPS for believable agent interactions
5. **Episode Logging & Replay**: Record entire "episodes" and replay them with timeline scrubbing

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Web UI Layer (Next.js/React)            │
│  ┌──────────────┬──────────────┬─────────────────┐  │
│  │ Scene        │ Agent        │ Episode Viewer  │  │
│  │ Designer     │ Studio       │ (Timeline)      │  │
│  └──────────────┴──────────────┴─────────────────┘  │
└─────────────────────────────────────────────────────┘
          │ REST API / WebSocket │
┌─────────────────────────────────────────────────────┐
│          Backend Services (FastAPI/Python)          │
│  ┌──────────────┬──────────────┬─────────────────┐  │
│  │ World Gen    │ Agent Engine │ Physics Engine  │  │
│  │ (LLM-based)  │ (PPO + Mem)  │ (Custom/Bullet) │  │
│  └──────────────┴──────────────┴─────────────────┘  │
│  ┌──────────────────────────────────────────────┐   │
│  │ Episode Logger & Replay System (JSON)       │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
          │ WebGL Rendering │
┌─────────────────────────────────────────────────────┐
│         3D Rendering Layer (Three.js/Babylon)       │
│  - Real-time 720p @ 24-60 FPS
│  - WebGL/WebGPU compatible
│  - Anime-style rendering pipeline
└─────────────────────────────────────────────────────┘
```

## Key Components

### 1. Scene Designer
- **Input**: Text prompts with scene parameters
- **Output**: Procedural 3D world in WebGL
- **Examples**:
  - "Rainy Tokyo rooftop at midnight with neon signs"
  - "Cyberpunk underground facility with holographic displays"
  - "Peaceful forest clearing with natural lighting"

### 2. Agent Studio
- Define agent archetypes with:
  - **Personality**: Traits affecting behavior weights
  - **Goals**: Primary/secondary objectives as reward signals
  - **Memory**: Long-term (learned policies) + short-term (observations)
  - **Embodiment**: Physical properties, animation rig

### 3. World Generation Pipeline
1. Parse text prompt with vision-language model
2. Extract: lighting, geometry, materials, physics properties
3. Generate scene graph via diffusion or procedural methods
4. Populate with assets from library
5. Initialize physics constraints

### 4. Agent Simulation Engine
- **Policy Network**: Simple neural net trained via PPO
- **Observation Space**: Agent's local sensor data
  - Visual field (camera)  
  - Proximity sensors
  - Event memory (past interactions)
- **Action Space**: Movement, rotation, interaction
- **Reward Function**: Weighted combination of:
  - Goal achievement
  - Narrative constraints
  - Physics plausibility

### 5. Episode Logger
- Real-time capture of:
  - Agent positions/states
  - Physics data
  - Event markers (goal achievement, collisions)
  - Agent "thoughts" (policy decisions)
- JSON-serializable format for replay
- Automatic scene generation metrics

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ (React 18)
- **3D Graphics**: Three.js / Babylon.js
- **State**: Zustand / Recoil
- **Styling**: TailwindCSS
- **API Client**: TanStack Query + WebSocket

### Backend  
- **Framework**: FastAPI (Python 3.10+)
- **LLM Integration**: OpenAI API / Hugging Face
- **Agent Engine**: Custom PyTorch implementation
- **Physics**: Pybullet / Nvidia PhysX
- **Database**: PostgreSQL for episode storage
- **Cache**: Redis for real-time state

### DevOps
- **Containerization**: Docker + Docker Compose
- **Deployment**: Vercel (frontend) + Railway/Heroku (backend)
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker (optional)

### Installation

```bash
# Clone repo
git clone https://github.com/yourusername/ai-drama-world-lab.git
cd ai-drama-world-lab

# Frontend setup
cd frontend
npm install

# Backend setup  
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Locally

```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend  
npm run dev
```

Access the app at `http://localhost:3000`

## Project Structure

```
ai-drama-world-lab/
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── SceneDesigner.tsx
│   │   │   ├── AgentStudio.tsx
│   │   │   └── EpisodeViewer.tsx
│   │   ├── pages/
│   │   └── layout.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── scene-generator.ts  # Three.js initialization
│   │   └── agent-visualizer.ts
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── worlds.py
│   │   │   ├── agents.py
│   │   │   └── episodes.py
│   │   ├── core/
│   │   │   ├── agent.py  # Agent class w/ policies
│   │   │   ├── world.py
│   │   │   └── physics.py
│   │   └── services/
│   │       ├── world_gen.py
│   │       ├── agent_engine.py
│   │       └── episode_logger.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Features (Roadmap)

- [ ] Text-to-3D world generation (Genie 3 integration)
- [ ] Multi-agent reinforcement learning
- [ ] Story-aware reward shaping
- [ ] Anime character import pipeline
- [ ] Multi-user collaborative mode
- [ ] Episode diffusion (generate variations)
- [ ] Cloud rendering (GPU acceleration)

## Contributing

This is an open research project. Contributions welcome! See CONTRIBUTING.md

## License

MIT License - See LICENSE file

## Acknowledgments

Inspired by:
- Genie 3 (world models)
- Dreamer v3 (world models + RL)
- VLMs for scene understanding
- Anime as narrative art form

