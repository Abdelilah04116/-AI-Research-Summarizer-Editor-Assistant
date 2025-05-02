"""
Data models for the application
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ResearchRequest(BaseModel):
    """Request model for research"""
    topic: str
    depth: Optional[str] = "medium"
    focus_areas: Optional[List[str]] = []


class ResearchResponse(BaseModel):
    """Response model for research results"""
    topic: str
    research_data: Dict[str, Any]
    summary: str
    final_report: str
    status: str = "complete"