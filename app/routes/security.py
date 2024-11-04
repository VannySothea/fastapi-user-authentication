from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.models.user import User
from app.config.auth import oauth2_scheme, get_current_user
from app.responses.security import AllDevicesResponse
from app.services.security import get_active_sessions, device_removal, device_removal_all
from typing import List
from app.schemas.security import DeviceRemove
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.async_database import get_async_session


auth_router = APIRouter(
    prefix="/security",
    tags=["Security"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)


@auth_router.get("/all-devices", response_model=List[AllDevicesResponse])
async def fetch_user(user = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    return await get_active_sessions(user.user_id, session)


@auth_router.delete("/logout-devices", status_code=status.HTTP_204_NO_CONTENT)
async def logout_device(data: DeviceRemove, user = Depends(get_current_user), session: AsyncSession  = Depends(get_async_session)):
    await device_removal(data.device_id, user.user_id, session)


@auth_router.delete("/logout-devices-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_device(user = Depends(get_current_user), session: AsyncSession  = Depends(get_async_session)):
    await device_removal_all(user.user_id, session)
