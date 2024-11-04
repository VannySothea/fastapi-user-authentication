from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class VerifyUserRequest(BaseModel):
    verification_code: str
    email: EmailStr


class EmailRequest(BaseModel):
    email: EmailStr


class VerifyForgotPassword(BaseModel):
    verification_code: str
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    verification_code: str
    email: EmailStr
    new_password: str
