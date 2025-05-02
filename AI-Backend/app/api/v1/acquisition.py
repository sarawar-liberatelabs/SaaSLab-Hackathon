from fastapi import APIRouter, Depends, HTTPException, status
from app.services.llm import get_openai_llm
from langchain_core.messages import HumanMessage, AIMessage
from app.curd.message_crud import store_chat_message, get_chat_history
from app.middleware.middleware import logger
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.chat_history import (
    ChatHistoryRequest,
    ChatHistoryResponse,
    StoreMessageInput
)
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.acquisition import Acquisition_Input, Acquisition_Response
from app.schemas.acquisition_state import AcquisitionState
from app.graph.acquisition_flow import AcquisitionGraph

AcquisitionRouter = APIRouter()

@AcquisitionRouter.post("/Acquisition", response_model=Acquisition_Response)
def chat(input_data: Acquisition_Input, db: Session = Depends(get_db)):
    """
    Chat endpoint that processes user input using the ChatOpenAI model and
    stores messages (human & AI) in the database.
    """
    try:
        
        result = AcquisitionGraph.invoke(
            AcquisitionState(
                thread_id=input_data.thread_id,
                message=input_data.message,
                response=""),
            config={"configurable": {"thread_id": str(input_data.thread_id)}}
        )


        # Store the interaction in the database with proper typing
        store_chat_message(
            StoreMessageInput(
                thread_id=input_data.thread_id,
                message_type="HumanMessage",
                message=str(input_data.message)  
            ),
            db,
        )

        store_chat_message(
            StoreMessageInput(
                thread_id=input_data.thread_id,
                message_type="AIMessage",
                message=result["response"]
            ),
            db,
        )

        return Acquisition_Response(
            thread_id=input_data.thread_id,
            response=result["response"]
        )

    except ValueError as ve:
        logger.error(f"Value error in chat endpoint: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail="Invalid input format")
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


