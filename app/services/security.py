from fastapi import HTTPException, status
from app.models.user import UserToken
from datetime import datetime
from sqlalchemy.future import select

# User Security Management
async def get_active_sessions(user_id, session):
    active_sessions = (await session.execute(select(UserToken).where(
        UserToken.user_id == user_id,
        UserToken.expires_at > datetime.utcnow()
    ))).scalars().all()

    return [
        {
            "device_id": token.device_id,
            "device_name": token.device_name,
            "created_at": token.created_at,
            "last_used_at": token.last_used_at,
        }
        for token in active_sessions
    ]


async def device_removal(device_id, user_id, session):
    user_token = (await session.execute(select(UserToken).where(
        UserToken.user_id == user_id,
        UserToken.device_id == device_id
    ))).scalars().first()

    if user_token:
        await session.delete(user_token)
        await session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found.")
    

async def device_removal_all(user_id, session):
    user_tokens = (await session.execute(select(UserToken).where(
        UserToken.user_id == user_id
    ))).scalars().all()

    for token in user_tokens:
        await session.delete(token)
    await session.commit()
