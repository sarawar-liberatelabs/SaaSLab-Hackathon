# from datetime import timedelta
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.auth.auth import authenticate_user, create_access_token
# from app.schemas.auth import Token
# from app.core.config import settings

# router = APIRouter()

# @router.post("/login", response_model=Token)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     """Login endpoint that returns a JWT token."""
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
    
#     return Token(access_token=access_token) 