from fastapi import APIRouter, HTTPException, status, Response, Depends, BackgroundTasks, Header, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.async_database import get_async_session
from app.responses.user import UserResponse, LoginResponse
from app.schemas.user import RegisterUserRequest, VerifyUserRequest, EmailRequest, VerifyForgotPassword, ResetPasswordRequest
from app.services.user import create_user_account, activate_user_account, get_login_token, get_refresh_token, email_forgot_password_link, reset_user_password, fetch_user_detail, verify_forgot_user_password
from app.models.user import User
from app.config.auth import oauth2_scheme, get_current_user, get_role_dependency
from app.config.security import validate_device_and_apply_rate_limiters
from typing import List
import logging
from sqlalchemy.future import select


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)

business_router = APIRouter(
    prefix="/business",
    tags=["Business"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_role_dependency(required_role="business_user"))]
)

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_role_dependency(required_role="admin"))]
)


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(request: Request, data: RegisterUserRequest, background_tasks: BackgroundTasks, device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):
    
    logging.info(f"Session type in register_user: {type(session)}")
    await validate_device_and_apply_rate_limiters(request, "register_user", device_id=device_id)
    return await create_user_account(request, data, background_tasks, device_id, session)


@user_router.post("/verify-account", status_code=status.HTTP_200_OK)
async def verify_user_account(request: Request, data: VerifyUserRequest, background_tasks: BackgroundTasks, device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):

    await validate_device_and_apply_rate_limiters(request, "verify_user_account", device_id=device_id)
    await activate_user_account(request, data, background_tasks, device_id, session)
    return {"Message": "Account is activated successfully"}


@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user(request: Request, data: OAuth2PasswordRequestForm = Depends(), device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):

    await validate_device_and_apply_rate_limiters(request, "login_user", device_id=device_id)
    return await get_login_token(request, data, device_id, session)


@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(request: Request, refresh_token=Header(), device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):

    await validate_device_and_apply_rate_limiters(request, "refresh_token", device_id=device_id)
    return await get_refresh_token(request, refresh_token, device_id, session)


@guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks, request: Request, device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):

    await validate_device_and_apply_rate_limiters(request, "forgot_password", device_id=device_id)
    await email_forgot_password_link(data, background_tasks, request, device_id, session)
    return {"Message": "An email with 6-digit code has been sent to you."}


@guest_router.post("/verify-forgot-password-code", status_code=status.HTTP_200_OK)
async def verify_forgot_password_code(data: VerifyForgotPassword, request: Request, device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):

    await validate_device_and_apply_rate_limiters(request, "verify_forgot_password", device_id=device_id)
    return await verify_forgot_user_password(data, request, device_id, session)


@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetPasswordRequest, background_tasks: BackgroundTasks, request: Request, device_id: str = Header(...), session: AsyncSession = Depends(get_async_session)):

    await validate_device_and_apply_rate_limiters(request, "reset_password", device_id=device_id)
    await reset_user_password(data, background_tasks, request, device_id, session)
    return {"Message": "Your password has been updated"}


@auth_router.get("/all", response_model=List[UserResponse])
async def fetch_all_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()  # Fetch all users from the result
    return users

@auth_router.get("/me", response_model=UserResponse)
async def fetch_current_user(user: UserResponse = Depends(get_current_user)):
    return user

@auth_router.get("/{id}", response_model=UserResponse)
async def fetch_user_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    return await fetch_user_detail(id, session)


@user_router.get("/client-ip")
async def get_client_ip(request: Request):
    client_ip = request.client.host # Get the client's IP address
    return {"client_ip": client_ip}
