# API Reference

## Base URL
```
http://localhost:8000/api
```

## World Generation API

### Generate World from Prompt

**Endpoint:** `POST /world/generate`

**Description:** Generate a 3D world scene from a text description.

**Request Body:**
```json
{
  "prompt": "A cozy indoor room with furniture",
  "seed": 42
}
```

**Response:** Returns a WorldScene object with generated 3D objects, lighting, and physics configuration.

### List World Templates

**Endpoint:** `GET /world/templates`

**Response:** Returns available scene templates.

## Agent API

### Create Agent
**Endpoint:** `POST /agents/create`

### List All Agents
**Endpoint:** `GET /agents/list`

### Get Agent by ID
**Endpoint:** `GET /agents/{agent_id}`

### Step Agent Simulation
**Endpoint:** `POST /agents/{agent_id}/step`

### Train Agent
**Endpoint:** `POST /agents/{agent_id}/train`

### Reset Agent
**Endpoint:** `POST /agents/{agent_id}/reset`

### Delete Agent
**Endpoint:** `DELETE /agents/{agent_id}`

## Episode API

### Start Episode Recording
**Endpoint:** `POST /episodes/start`

### Log Frame
**Endpoint:** `POST /episodes/log`

### End Episode Recording
**Endpoint:** `POST /episodes/end`

### List Episodes
**Endpoint:** `GET /episodes/list`

### Get Episode
**Endpoint:** `GET /episodes/{episode_id}`

### Get Episode Frames
**Endpoint:** `GET /episodes/{episode_id}/frames`

### Delete Episode
**Endpoint:** `DELETE /episodes/{episode_id}`

## WebSocket API

**Endpoint:** `WS /ws`

For detailed API examples and request/response schemas, visit http://localhost:8000/docs when running the application.
