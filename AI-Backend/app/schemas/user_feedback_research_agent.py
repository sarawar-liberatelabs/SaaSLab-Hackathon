from pydantic import BaseModel, Field
from typing import List, Dict, Any

class UserFeedbackResearchAgentInput(BaseModel):
    thread_id: str
    feedback_transcripts: List[str]
    support_logs: List[Dict[str, Any]]
    nps_data: List[Dict[str, Any]]


class UserFeedbackResearchAgentOutput(BaseModel):
    thread_id: int
    response: str
