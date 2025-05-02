"""
Utility functions for the application
"""
import os
from typing import Dict, Any


def validate_api_key(api_key: str) -> bool:
    """Validate OpenAI API key"""
    if not api_key or len(api_key) < 10:
        return False
    return True


def get_api_key() -> str:
    """Get API key from environment variables"""
    return os.environ.get("OPENAI_API_KEY", "")
