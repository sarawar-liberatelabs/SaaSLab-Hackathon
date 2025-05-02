from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class Acquisition_Input(BaseModel):
    thread_id: str  # Keep as string for API flexibility
    message: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class Acquisition_Response(BaseModel):
    thread_id: str  # Keep as string for API consistency
    response: str

    model_config = ConfigDict(from_attributes=True)
