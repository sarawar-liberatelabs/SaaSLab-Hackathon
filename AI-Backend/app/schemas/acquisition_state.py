from pydantic import BaseModel
from typing import Dict, Any
class AcquisitionState(BaseModel):
    thread_id: str
    message: dict [str, Any]
    response: str = None