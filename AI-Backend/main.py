from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.acquisition import AcquisitionRouter
from app.api.v1.chat import ChatRouter
from app.api.v1.user_feedback_research_agent import UserFeedbackResearchAgentRouter



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SaaSLab",
)



app.include_router(ChatRouter, tags=["Chat"])
app.include_router(AcquisitionRouter, tags=["Acquisition"])
app.include_router(UserFeedbackResearchAgentRouter, tags=["User Feedback Research Agent"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}

