from fastapi import BackgroundTasks
from app.models.user import User, VerificationCode, VerificationCodeOpt
from app.config.email import send_email
from app.config.settings import app_settings
from app.config.wrapper import generate_verification_code
from sqlalchemy.orm import Session


async def send_account_verification_email(user: User, db: Session , background_tasks: BackgroundTasks):
    verification_code = await generate_verification_code(VerificationCodeOpt, user, db)
    data = {
        'app_name': app_settings.APP_NAME,
        "company_name": app_settings.COMPANY_NAME,
        "user_name": user.user_name,
        'verification_code': verification_code
    }

    subject = f"{verification_code} is your {app_settings.APP_NAME} verification code"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="account-verification.html",
        context=data,
        background_tasks=background_tasks
    )
    
    
async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        'app_name': app_settings.APP_NAME,
        "company_name": app_settings.COMPANY_NAME,
        "user_name": user.user_name,
    }
    subject = f"Welcome - {app_settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks
    )
    

async def send_password_reset_email(user: User, db: Session , background_tasks: BackgroundTasks):
    verification_code = await generate_verification_code(VerificationCode, user, db)
    data = {
        'app_name': app_settings.APP_NAME,
        "company_name": app_settings.COMPANY_NAME,
        "user_name": user.user_name,
        'verification_code': verification_code,
    }
    subject = f"{verification_code} is your {app_settings.APP_NAME} verification code"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="password-reset.html",
        context=data,
        background_tasks=background_tasks
    )


async def password_reset_successful(user: User, db: Session , background_tasks: BackgroundTasks):
    data = {
        'app_name': app_settings.APP_NAME,
        "company_name": app_settings.COMPANY_NAME,
        "user_name": user.user_name
    }
    subject = f"Password Reset Successfully - {app_settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="password-reset-successful.html",
        context=data,
        background_tasks=background_tasks
    )
    