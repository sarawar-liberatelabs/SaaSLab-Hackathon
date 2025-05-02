from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.db.database import init_db
from app.api.v1.chat import ChatRouter
from app.middleware.middleware import add_logger_middleware
from app.api.v1.acquisition import AcquisitionRouter



init_db()


app = FastAPI(
        title="AI Dermatology Assistant API",
        description="",
        version="1.0.0"
    )
add_logger_middleware(app)



# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(UsersRouter, prefix="/user", tags=["Users"])
app.include_router(ChatRouter, prefix="/chat", tags=["Chat"])
app.include_router(AcquisitionRouter, tags=["Acquisition"])



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")