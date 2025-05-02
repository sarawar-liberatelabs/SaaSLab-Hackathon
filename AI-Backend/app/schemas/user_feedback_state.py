from pydantic import BaseModel
from typing import List, Dict, Any

class UserFeedbackState(BaseModel):
    thread_id: str
    feedback_transcripts: List[str]
    support_logs: List[Dict[str, Any]]
    nps_data: List[Dict[str, Any]]
    response: str
