from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class A2AState(BaseModel):
    trace_id: str
    parent_observation_id: Optional[str] = None
    current_agent: str
    next_agent: Optional[str] = None
    data: Dict[str, Any]
    status: str  # e.g., "pending", "processing", "completed", "error"
    timestamp: datetime = datetime.utcnow()
    user_query: str
    # Add more fields as needed for the ecosystem