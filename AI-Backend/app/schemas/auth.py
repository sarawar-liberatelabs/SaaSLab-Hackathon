# from pydantic import BaseModel, EmailStr, Field
# from datetime import datetime
# from typing import Optional

# class Token(BaseModel):
#     access_token: str
#     token_type: str = "bearer"

# class TokenData(BaseModel):
#     username: Optional[str] = None
#     exp: Optional[datetime] = None

# class LoginInput(BaseModel):
#     username: str = Field(..., min_length=3, max_length=50)
#     password: str = Field(..., min_length=6, max_length=128)

# class UserAuth(BaseModel):
#     username: str
#     email: EmailStr
#     disabled: bool = False 