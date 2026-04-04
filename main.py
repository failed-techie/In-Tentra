"""
INTENTRA - Multi-Agent AI Trading System
Main FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from db.database import init_db, get_db
from config.settings import settings
from agents.master_agent import MasterAgent

# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    print("Database initialized")
    yield
    # Shutdown: Cleanup resources
    print("Shutting down INTENTRA")

app = FastAPI(
    title="INTENTRA",
    description="Multi-Agent AI Trading System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "INTENTRA is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Trading intent endpoint
@app.post("/intent/submit")
async def submit_intent(intent: dict):
    """Submit a trading intent for processing"""
    try:
        master = MasterAgent()
        result = await master.process_intent(intent)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get intent status
@app.get("/intent/{intent_id}")
async def get_intent_status(intent_id: str):
    """Get the status of a submitted intent"""
    # TODO: Implement intent status retrieval
    return {"intent_id": intent_id, "status": "pending"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
