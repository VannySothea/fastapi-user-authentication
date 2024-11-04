from app.responses.base import BaseResponse
from pydantic import EmailStr
from datetime import datetime
from typing import Union


class UserResponse(BaseResponse):
    user_id: int
    user_name: str
    email: EmailStr
    created_at: Union[str, None, datetime] = None


class LoginResponse(BaseResponse):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"
    
