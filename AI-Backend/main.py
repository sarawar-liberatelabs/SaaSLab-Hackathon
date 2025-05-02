from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.api.v1.acquisition import AcquisitionRouter
from app.api.v1.chat import ChatRouter
from app.api.v1.user_feedback_research_agent import UserFeedbackResearchAgentRouter
from app.middleware.middleware import add_logger_middleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SaaSLab",
)

add_logger_middleware(app)

app.include_router(ChatRouter, tags=["Chat"])
app.include_router(AcquisitionRouter, tags=["Acquisition"])
app.include_router(UserFeedbackResearchAgentRouter, tags=["User Feedback Research Agent"])

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
