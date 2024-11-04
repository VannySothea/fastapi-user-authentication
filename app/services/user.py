from fastapi import HTTPException, Response, status
from app.models.user import User, UserToken, VerificationCode, RegistrationRequest, VerificationCodeOpt, Code, Role
from app.config.auth import hash_password, verify_password, load_user, generate_token, get_token_payload, str_decode, str_encode, delete_expired_tokens, check_active_sessions, revoke_oldest_session, delete_exist_token, get_user_token
from app.config.wrapper import generate_verification_code, delete_existing_verification_code, check_verification_codes
from app.config.settings import settings, app_settings
from app.services.email import send_account_verification_email, send_account_activation_confirmation_email, send_password_reset_email, password_reset_successful
from datetime import datetime, timedelta
import logging
from app.utils.string import unique_string
from app.config.role import normal_user
from app.config.security import record_device_lockout_attempt, record_ip_lockout_attempt, apply_device_lockout, apply_ip_lockout
import logging
from sqlalchemy.future import select
from app.services.security import device_removal_all


async def create_user_account(request, data, background_tasks, device_id, session):
    # logging.info(f"Session type: {type(session)}")
    await apply_device_lockout(device_id, operation="create_user_account")
    await apply_ip_lockout(request, operation="create_user_account")
    activated_account = await load_user(User, data.email, session)

    if activated_account:
        await record_device_lockout_attempt(device_id, operation="create_user_account")
        await record_ip_lockout_attempt(request, operation="create_user_account")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The account is already existed")

    existed_account = await load_user(RegistrationRequest, data.email, session)
    if existed_account:
        existed_account.password = await hash_password(data.password)
        existed_account.user_name = data.user_name
        existed_account.created_at = datetime.utcnow()
        session.add(existed_account)
        await session.commit()
        await session.refresh(existed_account)

        # Delete existed virification code created by the same user
        await delete_existing_verification_code(VerificationCodeOpt, existed_account.user_id, session)
        
        await send_account_verification_email(existed_account, session, background_tasks=background_tasks)
        return existed_account
    
    register_user = RegistrationRequest(**data.model_dump())
    register_user.password = await hash_password(data.password)
    
    session.add(register_user)
    await session.commit()
    await session.refresh(register_user)

    # Delete existed virification code created by the same user
    await delete_existing_verification_code(VerificationCodeOpt, register_user.user_id, session)

    await send_account_verification_email(register_user, session, background_tasks=background_tasks)
    return register_user


async def activate_user_account(request, data, background_tasks, device_id, session):

    await apply_device_lockout(device_id, operation="activate_user_account")
    await apply_ip_lockout(request, operation="activate_user_account")
    
    request_user = await load_user(RegistrationRequest, data.email, session)
    if not request_user:
        await record_device_lockout_attempt(device_id, operation="activate_user_account")
        await record_ip_lockout_attempt(request, operation="activate_user_account")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid verification code, either expired or not valid.")

    # Check for the verification code
    code_record = await check_verification_codes(VerificationCodeOpt, data.verification_code, request_user.user_id, session)
    if not code_record:
        await record_device_lockout_attempt(device_id, operation="activate_user_account")
        await record_ip_lockout_attempt(request, operation="activate_user_account")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code, either expired or not valid.")

    user = User()
    user.user_id = request_user.user_id
    user.user_name = request_user.user_name
    user.email = request_user.email
    user.password = request_user.password
    user.roles.append(await normal_user(session))
    # if (request_user.email == "vannysothea070@gmail.com"):
    #     user.roles.append(await admin(session))
    user.verified_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()
    user.created_at = request_user.created_at
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Delete or invalidate the used code
    await delete_existing_verification_code(VerificationCodeOpt, request_user.user_id, session)

    # Delete user from RegistrationRequest table
    await session.delete(request_user)
    await session.commit()

    # Send account activation confirmation email
    await send_account_activation_confirmation_email(user, background_tasks=background_tasks)

    return user


async def get_login_token(request, data, device_id, session):

    await apply_device_lockout(device_id, operation="get_login_token")
    await apply_ip_lockout(request, operation="get_login_token")
    
    user = await load_user(User, data.username, session)

    if not user:
        await record_device_lockout_attempt(device_id, operation="get_login_token")
        await record_ip_lockout_attempt(request, operation="get_login_token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password.")

    valid_password = await verify_password(data.password, user.password)
    if not valid_password:
        await record_device_lockout_attempt(device_id, operation="get_login_token")
        await record_ip_lockout_attempt(request, operation="get_login_token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password.")
    
    
    # Check if a token already exists for this user and device_id if exists delete it
    await delete_exist_token(UserToken, user.user_id, device_id, session)

    # Check if the account reach maximum devices, if it reaches, revoke the oldest session and create the new one
    MAX_DEVICES = 5
    active_token = await check_active_sessions(user.user_id, session)

    if(active_token >= MAX_DEVICES):
        await revoke_oldest_session(user.user_id, session)

    return await _generate_tokens(user, device_id, session)


async def get_refresh_token(request, refresh_token, device_id, session):

    await apply_device_lockout(device_id, operation="get_refresh_token")
    await apply_ip_lockout(request, operation="get_refresh_token")
    token_payload = await get_token_payload(refresh_token, settings.SECRET_KEY, app_settings.JWT_ALGORITHM)
    if not token_payload:
        await record_device_lockout_attempt(device_id, operation="get_refresh_token")
        await record_ip_lockout_attempt(request, operation="get_refresh_token")
        logging.error("Failed to decode refresh token.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request.")
    
    refresh_key = token_payload.get("t") #refresh key
    access_key = token_payload.get("a") #access key
    user_id = await str_decode(token_payload.get("sub")) #user_id


    user_token = await get_user_token(UserToken, refresh_key, access_key, user_id, device_id, session)
    
    if not user_token: 
        await record_device_lockout_attempt(device_id, operation="get_refresh_token")
        await record_ip_lockout_attempt(request, operation="get_refresh_token")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Request.")

    
    user_token.expires_at = datetime.utcnow()
    session.add(user_token)
    await session.commit()
    # Delete the expired token
    await delete_expired_tokens(session)

    return await _generate_tokens(user_token.user, device_id, session)


async def _generate_tokens(user, device_id, session):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=app_settings.REFRESH_TOKEN_EXPIRE_MINUTES) #1440

    user_token = UserToken()
    user_token.user_id = user.user_id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.device_id = device_id
    user_token.expires_at = datetime.utcnow() + rt_expires
    user_token.last_used_at = datetime.now()
    session.add(user_token)
    await session.commit()
    await session.refresh(user_token)

    at_payload = {
        "sub": await str_encode(str(user.user_id)),
        "a": access_key,
        "r": await str_encode(str(user_token.id)),
        "n": await str_encode(f"{user.user_name}")
    }
    
    at_expires = timedelta(minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES) #3
    access_token = await generate_token(at_payload, settings.JWT_SECRET, app_settings.JWT_ALGORITHM, at_expires)

    rt_payload = {
        "sub": await str_encode(str(user.user_id)),
        "t": refresh_key,
        "a": access_key
    }
    refresh_token = await generate_token(rt_payload, settings.SECRET_KEY, app_settings.JWT_ALGORITHM, rt_expires)

    # logging.info(f"Access Token: {access_token}")
    # logging.info(f"Refresh Token: {refresh_token}")


    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }

async def email_forgot_password_link(data, background_tasks, request, device_id, session):
    await apply_device_lockout(device_id, operation="email_forgot_password_link")
    await apply_ip_lockout(request, operation="email_forgot_password_link")
    user = await load_user(User, data.email, session)
    if not user:
        await record_device_lockout_attempt(device_id, operation="email_forgot_password_link")
        await record_ip_lockout_attempt(request, operation="email_forgot_password_link")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email")
    
    # Delete existed virification code created by the same user
    await delete_existing_verification_code(VerificationCode, user.user_id, session)
    
    await send_password_reset_email(user, session, background_tasks=background_tasks)
    return user

async def verify_forgot_user_password(data, request, device_id, session):
    await apply_device_lockout(device_id, operation="verify_forgot_user_password")
    await apply_ip_lockout(request, operation="verify_forgot_user_password")
    user = await load_user(User, data.email, session)
    if not user:
        await record_device_lockout_attempt(device_id, operation="verify_forgot_user_password")
        await record_ip_lockout_attempt(request, operation="verify_forgot_user_password")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid verification code, either expired or not valid.")
    
    # Check for the verification code
    code_record = await check_verification_codes(VerificationCode, data.verification_code, user.user_id, session)
    if not code_record:
        await record_device_lockout_attempt(device_id, operation="verify_forgot_user_password")
        await record_ip_lockout_attempt(request, operation="verify_forgot_user_password")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code, either expired or not valid.")
    
    # Delete existed virification code
    await delete_existing_verification_code(VerificationCode, user.user_id, session)

    verification_code = await generate_verification_code(Code, user, session)
    return {"code": verification_code}

async def reset_user_password(data, background_tasks, request, device_id, session):
    await apply_device_lockout(device_id, operation="reset_user_password")
    await apply_ip_lockout(request, operation="reset_user_password")
    user = await load_user(User, data.email, session)
    if not user:
        await record_device_lockout_attempt(device_id, operation="reset_user_password")
        await record_ip_lockout_attempt(request, operation="reset_user_password")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code, either expired or not valid.")
    
    # Check for the verification code
    code_record = await check_verification_codes(Code, data.verification_code, user.user_id, session)
    if not code_record:
        await record_device_lockout_attempt(device_id, operation="reset_user_password")
        await record_ip_lockout_attempt(request, operation="reset_user_password")
        # logging.warning(f"{Code.code} = {data.verification_code}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code, either expired or not valid.")
    

    user.password = await hash_password(data.new_password)
    user.updated_at = datetime.utcnow()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    # Delete or invalidate the used code here
    await delete_existing_verification_code(Code, user.user_id, session)
    await device_removal_all(user.user_id, session)
    await password_reset_successful(user, session, background_tasks=background_tasks)


async def fetch_user_detail(id, session):
    stmt = select(User).where(User.user_id == id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists.")
