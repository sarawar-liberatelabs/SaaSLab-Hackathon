from sqlalchemy import asc
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.chat_history import ChatHistory
from app.schemas.chat_history import StoreMessageInput, ChatHistoryRequest, ChatHistoryItem

def store_chat_message(input_text: StoreMessageInput, db: Session):
    """
    Inserts a chat message into the database.
    """
    db_chat = ChatHistory(
        thread_id=input_text.thread_id,
        message=input_text.message,
        message_type=input_text.message_type,
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return db_chat

def get_chat_history(input_text: ChatHistoryRequest, db: Session):
    """
    Retrieves chat history for a specific thread_id,
    with pagination support.
    """    
    # Create the base query
    query = db.query(ChatHistory)
    
    # Apply thread_id filter
    query = query.filter(ChatHistory.thread_id == input_text.thread_id)
    
    # Order by timestamp ascending (oldest first)
    query = query.order_by(asc(ChatHistory.timestamp))
    
    # Apply pagination
    chat_entries = query.offset(input_text.skip).limit(input_text.limit).all()
    
    # Convert to ChatHistoryItem objects
    return [
        ChatHistoryItem(
            id=entry.id,
            thread_id=entry.thread_id,
            message=entry.message,
            message_type=entry.message_type,
            timestamp=entry.timestamp.isoformat() if entry.timestamp else None
        )
        for entry in chat_entries
    ]
