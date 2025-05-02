from fastapi import APIRouter, Depends, HTTPException
from app.curd.message_crud import store_chat_message
from app.middleware.middleware import logger
from app.schemas.user_feedback_research_agent import UserFeedbackResearchAgentInput, UserFeedbackResearchAgentOutput
from app.schemas.chat_history import StoreMessageInput
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.graph.user_feedback_flow import UserFeedbackGraph
from app.schemas.user_feedback_state import UserFeedbackState

UserFeedbackResearchAgentRouter = APIRouter()

@UserFeedbackResearchAgentRouter.post("/UserFeedbackResearchAgentRouter", response_model=UserFeedbackResearchAgentOutput)
def chat(input_data: UserFeedbackResearchAgentInput, db: Session = Depends(get_db)):
    """
    Chat endpoint that processes user input using the ChatOpenAI model and
    stores messages (human & AI) in the database.
    """
    try:
        result = UserFeedbackGraph.invoke(
            UserFeedbackState(
            thread_id=input_data.thread_id,
            feedback_transcripts=input_data.feedback_transcripts,
            support_logs=input_data.support_logs,
            nps_data=input_data.nps_data,
            response="",
            ),
        config={"configurable": {"thread_id": str(input_data.thread_id)}}
        )




        # Store the interaction in the database with proper typing
        store_chat_message(
            StoreMessageInput(
                thread_id=input_data.thread_id,
                message_type="HumanMessage",
                message=str("Dummy input")  
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

        return UserFeedbackResearchAgentOutput(
            thread_id=input_data.thread_id,
            response=result["response"]
        )

    except ValueError as ve:
        logger.error(f"Value error in chat endpoint: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail="Invalid input format")
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


