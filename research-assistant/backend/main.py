"""
FastAPI backend for the Research Assistant
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from typing import Dict, Any, List
import uuid

from app.models import ResearchRequest, ResearchResponse
from app.crew import run_research_process
from app.utils import validate_api_key, get_api_key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Research Assistant API",
    description="API for a multi-agent research assistant system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Store for research tasks and results
research_tasks: Dict[str, Dict[str, Any]] = {}


@app.get("/")
async def read_root():
    """Root endpoint"""
    return {"message": "Research Assistant API"}


@app.post("/research", response_model=Dict[str, Any])
async def create_research(
    research_request: ResearchRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    """Start a research task"""
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    task_id = str(uuid.uuid4())
    research_tasks[task_id] = {
        "topic": research_request.topic,
        "status": "in_progress",
        "results": None
    }
    
    # Run research in background
    background_tasks.add_task(
        perform_research_task,
        task_id=task_id,
        topic=research_request.topic,
        focus_areas=research_request.focus_areas,
        api_key=api_key
    )
    
    return {"task_id": task_id, "status": "in_progress"}


@app.get("/research/{task_id}", response_model=Dict[str, Any])
async def get_research_status(task_id: str):
    """Get status or results of a research task"""
    if task_id not in research_tasks:
        raise HTTPException(status_code=404, detail="Research task not found")
    
    task_info = research_tasks[task_id]
    
    if task_info["status"] == "complete" and task_info["results"]:
        return {
            "task_id": task_id,
            "status": "complete",
            "topic": task_info["topic"],
            "results": task_info["results"]
        }
    elif task_info["status"] == "failed":
        return {
            "task_id": task_id,
            "status": "failed",
            "topic": task_info["topic"],
            "error": task_info.get("error", "Unknown error")
        }
    else:
        return {
            "task_id": task_id,
            "status": "in_progress",
            "topic": task_info["topic"]
        }


async def perform_research_task(task_id: str, topic: str, focus_areas: List[str], api_key: str):
    """Perform research task in background"""
    try:
        logger.info(f"Starting research on topic: {topic}")
        results = run_research_process(api_key, topic, focus_areas)
        
        # Update task info with results
        research_tasks[task_id]["status"] = "complete"
        research_tasks[task_id]["results"] = results
        logger.info(f"Research completed for task: {task_id}")
    
    except Exception as e:
        logger.error(f"Research failed for task {task_id}: {str(e)}")
        research_tasks[task_id]["status"] = "failed"
        research_tasks[task_id]["error"] = str(e)

