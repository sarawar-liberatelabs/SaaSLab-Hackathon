from fastapi import APIRouter, Depends, HTTPException, status
from app.services.llm import get_openai_llm
from langchain_core.messages import HumanMessage, AIMessage
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.curd.message_crud import store_chat_message, get_chat_history
from app.middleware.middleware import logger
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.chat_history import (
    ChatHistoryRequest,
    ChatHistoryResponse,
    StoreMessageInput
)
from app.schemas.chat import ChatInput, ChatResponse
from app.prompts.chat import BASIC_CHAT_PROMPT


ChatRouter = APIRouter()


@ChatRouter.post("/chat", response_model=ChatResponse)
def chat(
    input_data: ChatInput,
    db: Session = Depends(get_db)
):
    """
    Chat endpoint that processes user input using the ChatOpenAI model and
    stores messages (human & AI) in the database.
    """
    try:
        llm = get_openai_llm(model_name="gpt-4.1", temperature=0.0)
        prompt = ChatPromptTemplate.from_template(BASIC_CHAT_PROMPT)
        chain = prompt | llm
        response = chain.invoke({"message": input_data.message})

        store_chat_message(
            StoreMessageInput(
                thread_id=input_data.thread_id,
                message_type="HumanMessage",
                message=input_data.message
            ),
            db,
        )

        store_chat_message(
            StoreMessageInput(
                thread_id=input_data.thread_id,
                message_type="AIMessage",
                message=response.content
            ),
            db,
        )

        return ChatResponse(
            thread_id=input_data.thread_id,
            message=input_data.message,
            response=response.content
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@ChatRouter.post("/chat/history", response_model=ChatHistoryResponse)
def fetch_chat_history(
    query_params: ChatHistoryRequest,
    db: Session = Depends(get_db)):
    """
    Endpoint to retrieve chat history for the current user,
    filtered by chat_id, thread_id, skip, and limit.
    """
    try:
        chat_entries = get_chat_history(query_params, db=db)
        return ChatHistoryResponse(chat_history=chat_entries)
    except Exception as e:
        logger.error(f"Error in fetch_chat_history endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error.")