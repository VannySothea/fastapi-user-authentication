from contextlib import asynccontextmanager
from app.config.async_database import AsyncSessionLocal
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import random, string
from sqlalchemy import delete
from sqlalchemy.future import select

# database async content manager wrapper function
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        

# verification_code
async def delete_existing_verification_code(table_name, user_id, session):
    # Create a delete statement for the specified table
    stmt = delete(table_name).where(table_name.user_id == user_id)
    await session.execute(stmt)  # Execute the delete statement
    await session.commit()  # Commit the changes

async def check_verification_codes(table_name, input_verification_code, user_id, session):
    try:
        verification_code = (await session.execute(select(table_name).where(
            table_name.code == input_verification_code,
            table_name.user_id == user_id,
            table_name.expires_at > datetime.utcnow()
            )
        )).scalars().first()
    except Exception as code_exec:
        verification_code = None
    return verification_code

async def generate_verification_code(table_name, user, db: AsyncSession):
    verification_code = ''.join(random.choices(string.digits, k=6))
    expires_at = datetime.utcnow() + timedelta(seconds=180)  # Code valid for 3 minutes
    # Save verification code
    code_record = table_name(
        user_id=user.user_id,
        code=verification_code,
        expires_at=expires_at
    )
    db.add(code_record)
    await db.commit()
    return verification_code



# Wrapper function used by scheduler:
async def get_all_expired_verification_code(table_name, session):
    current_time = datetime.utcnow()
    # Fetch and delete expired verification codes
    expired_codes = (await session.execute(select(table_name).where(table_name.expires_at < current_time))).scalars().all()

    return expired_codes


async def delete_all_expired_verification_code(expired_codes, session):

    for code in expired_codes:
        await session.delete(code)
    await session.commit()