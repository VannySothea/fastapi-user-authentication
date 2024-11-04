from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import logging, base64
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Response, status
from app.config.async_database import get_async_session
from app.config.settings import settings, app_settings
from app.models.user import UserToken, UserToken
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from sqlalchemy.future import select
from typing import Callable, Awaitable, Any
from sqlalchemy import cast, Integer, String


JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = app_settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = app_settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Hashing handling
async def hash_password(password):
    return pwd_context.hash(password)

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Encryption/Decryption
async def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')

async def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


async def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {jwt_exec}, Token: {token}")  # Log the token for debugging
        payload = None
    
    return payload

# Token handling
async def delete_expired_tokens(session):
    # Create a delete statement for UserToken
    try:
        stmt = delete(UserToken).where(UserToken.expires_at < datetime.utcnow())
        await session.execute(stmt)  # Execute the delete statement
        await session.commit()  # Commit the changes
    except Exception as e:
        logging.error(f"Error to delete expired tokens: {str(e)}")

async def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.utcnow() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)

async def get_token_user(token: str, db: AsyncSession):
    try:
        payload = await get_token_payload(token, settings.JWT_SECRET, app_settings.JWT_ALGORITHM)
        if payload:
            user_token_id = int(await str_decode(payload.get('r')))  # Decode as integer
            user_id = int(await str_decode(payload.get('sub')))      # Decode as integer
            access_key = payload.get('a')

            user_token = (await db.execute(
                select(UserToken)
                .options(joinedload(UserToken.user))
                .where(
                    UserToken.access_key == access_key,
                    cast(UserToken.id, Integer) == user_token_id,  # Ensure correct casting
                    cast(UserToken.user_id, Integer) == user_id,    # Ensure correct casting
                    UserToken.expires_at > datetime.utcnow()
                )
            )).scalars().first()

            if user_token:
                return user_token.user
    except Exception as e:
        logging.error(f"Error in get_token_user: {str(e)}")
        return None
    return None

async def get_user_token(table_name, refresh_key, access_key, user_id, device_id, session):

    stmt = select(table_name).options(selectinload(table_name.user)).where(
        table_name.refresh_key == refresh_key,
        table_name.access_key == access_key,
        cast(table_name.user_id, Integer) == int(user_id),
        table_name.device_id == device_id,
        table_name.expires_at > datetime.utcnow()
    )

    result = await session.execute(stmt)
    user_token = result.scalars().first()

    return user_token

# Get user 
async def load_user(table_name, input_email: str, session):
    try:
        user = (await session.execute(select(table_name).where(table_name.email == input_email))).scalars().first()
    except Exception as user_exec:
        user = None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    user = await get_token_user(token=token, db=db)
    if user: 
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")

def get_role_dependency(required_role: str) -> Callable[..., Awaitable[Any]]:
    async def role_checker(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
        user = await get_current_user(token=token, db=db)
        if user:
            user_roles = [role.role_name for role in user.roles]
            if required_role in user_roles:
                return user
        
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this resource.")
    
    return role_checker

# device handling
async def check_active_sessions(user_id, session: AsyncSession) -> int:
    # Create a select statement to find all active tokens for the user
    stmt = select(UserToken).where(UserToken.user_id == user_id)
    result = await session.execute(stmt)  # Execute the statement asynchronously
    
    # Use list comprehension to collect the active tokens and get their count
    active_tokens = result.scalars().all()  # Get all active tokens
    active_token_count = len(active_tokens)  # Count the number of active tokens
    
    return active_token_count

async def revoke_oldest_session(user_id, session):

    stmt = select(UserToken).where(UserToken.user_id == user_id).order_by(UserToken.created_at.asc())
    result = await session.execute(stmt)  # Execute the statement asynchronously

    oldest_token = result.scalars().first()  # Get the oldest token

    if oldest_token:
        await session.delete(oldest_token)  # Delete the oldest token asynchronously
        await session.commit()  # Commit the transaction asynchronously

# Check if a token already exists for this user and device_id
async def delete_exist_token(table_name, user_id, device_id, session):
    
    stmt = select(table_name).where(
    table_name.user_id == user_id,
    table_name.device_id == device_id
    )
    result = await session.execute(stmt)
    existing_tokens = result.scalars().all()
    # Check if the token exists before trying to delete it
    if existing_tokens:
        for token in existing_tokens:
            await session.delete(token)
        await session.commit()
