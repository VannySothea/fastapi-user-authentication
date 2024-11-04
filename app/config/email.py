from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.background import BackgroundTasks
from app.config.settings import mail_settings


conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.MAIL_USERNAME,
    MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
    MAIL_PORT=mail_settings.MAIL_PORT,
    MAIL_SERVER=mail_settings.MAIL_SERVER,
    MAIL_STARTTLS=mail_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=mail_settings.MAIL_SSL_TLS,
    MAIL_DEBUG=mail_settings.MAIL_DEBUG,
    MAIL_FROM=mail_settings.MAIL_FROM,
    MAIL_FROM_NAME=mail_settings.MAIL_FROM_NAME,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=mail_settings.USE_CREDENTIALS
)

fm = FastMail(conf)


async def send_email(recipients: list, subject: str, context: dict, template_name: str,
                     background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
