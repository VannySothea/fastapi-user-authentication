from datetime import datetime, timedelta
from app.models.user import (
    RegistrationRequest, UserToken, VerificationCodeOpt, VerificationCode, Code
)
from app.config.wrapper import get_session, get_all_expired_verification_code, delete_all_expired_verification_code
import logging
from sqlalchemy.future import select


logging.basicConfig(level=logging.INFO)

# Cleanup last 24H user registration requests
async def cleanup_expired_user_registration_request():
    async with get_session() as session:
        threshold_date = datetime.now() - timedelta(hours=24)
        try:
            expired_users = (await session.execute(select(RegistrationRequest).where(RegistrationRequest.created_at < threshold_date))).scalars().all()
            for user in expired_users:
                await session.delete(user)
            await session.commit()

            logging.info(f"Deleted {len(expired_users)} registration requests users.")
        except Exception as e:
            logging.error(f"Failed to delete user registration requests: {e}")


# Cleanup expired user tokens job
async def cleanup_expired_user_tokens():
    async with get_session() as session:
        current_time = datetime.utcnow()
        try:
            expired_user_tokens = (await session.execute(select(UserToken).where(UserToken.expires_at < current_time))).scalars().all()
            for user_token in expired_user_tokens:
                await session.delete(user_token)
            await session.commit()

            logging.info(f"Deleted {len(expired_user_tokens)} expired user tokens.")
        except Exception as e:
            logging.error(f"Failed to delete expired user tokens: {e}")


# Cleanup expired verification codes job
async def cleanup_expired_verification_codes_opt():
    async with get_session() as session:
        try:
            # Fetch and delete expired verification codes
            expired_codes = await get_all_expired_verification_code(VerificationCodeOpt, session)

            await delete_all_expired_verification_code(expired_codes, session)
            
            logging.info(f"Deleted {len(expired_codes)} expired verification codes opt.")
        except Exception as e:
            logging.error(f"Failed to delete verification codes opt: {e}")

async def cleanup_expired_verification_codes():
    async with get_session() as session:
        try:
            # Fetch and delete expired verification codes
            expired_codes = await get_all_expired_verification_code(VerificationCode, session)

            await delete_all_expired_verification_code(expired_codes, session)
            
            logging.info(f"Deleted {len(expired_codes)} expired verification codes.")
        except Exception as e:
            logging.error(f"Failed to delete verification codes: {e}")

async def cleanup_expired_codes():
    async with get_session() as session:
        try:
            # Fetch and delete expired verification codes
            expired_codes = await get_all_expired_verification_code(Code, session)

            await delete_all_expired_verification_code(expired_codes, session)
            
            logging.info(f"Deleted {len(expired_codes)} expired 6-digit codes.")
        except Exception as e:
            logging.error(f"Failed to delete 6-digit codes: {e}")
