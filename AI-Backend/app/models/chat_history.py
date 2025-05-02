from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, index=True, nullable=False)
    message = Column(String, index=True)
    message_type = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
