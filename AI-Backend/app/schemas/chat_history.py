from pydantic import BaseModel, ConfigDict
from typing import Optional, List

    
class StoreMessageInput(BaseModel):
    thread_id: int
    message: str
    message_type: str

    model_config = ConfigDict(from_attributes=True)


class ChatHistoryRequest(BaseModel):
    thread_id: int
    skip: int = 0
    limit: int = 10

class ChatHistoryItem(BaseModel):
    id: int
    thread_id: int
    message: str
    message_type: str
    timestamp: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class ChatHistoryResponse(BaseModel):
    chat_history: List[ChatHistoryItem]

    model_config = ConfigDict(from_attributes=True)