import os
from pathlib import Path

class Config:
    # Core Agent Identity & Workspace Mapping
    VANE_ROOT_ID = os.getenv("VANE_ROOT_ID", "VANE_ROOT_ID_8A9B3C4D5E6F7G8H")
    BASE_DIR = Path(__file__).resolve().parent
    
    # Workspace isolation using the Vane Root ID
    WORKSPACE_DIR = BASE_DIR / "workspaces" / VANE_ROOT_ID
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIR = str(WORKSPACE_DIR / "chroma_db")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # LLM Orchestration
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "800"))
    
    # API Network Thresholds
    API_TIMEOUT = float(os.getenv("API_TIMEOUT", "3.5"))
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "4"))
    
    # Confidence Score Boundaries
    CONFIDENCE_HIGH_THRESHOLD = float(os.getenv("CONFIDENCE_HIGH_THRESHOLD", "0.85"))
    CONFIDENCE_MEDIUM_THRESHOLD = float(os.getenv("CONFIDENCE_MEDIUM_THRESHOLD", "0.60"))
