"""
AI Drama World Lab - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from api.world import router as world_router
from api.agents import router as agents_router
from api.episodes import router as episodes_router
from utils.websocket_manager import websocket_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting AI Drama World Lab Backend")
    yield
    logger.info("🛑 Shutting down AI Drama World Lab Backend")


app = FastAPI(
    title="AI Drama World Lab API",
    description="Backend API for AI-powered 3D drama world generation and agent simulation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(world_router, prefix="/api/world", tags=["World Generation"])
app.include_router(agents_router, prefix="/api/agents", tags=["Agents"])
app.include_router(episodes_router, prefix="/api/episodes", tags=["Episodes"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Drama World Lab API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive client messages
            data = await websocket.receive_text()
            logger.info(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
