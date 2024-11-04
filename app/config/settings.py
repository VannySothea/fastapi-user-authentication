from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # PostgreSQL Database Config
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    # JWT Secret Key
    JWT_SECRET: str

    # App Secret Key
    SECRET_KEY: str

    # OTP Secret Key
    # OTP_SECRET: str
    class Config:
        env_file = "env/.env.settings"



class AppSettings(BaseSettings):

    # App
    APP_NAME: str
    COMPANY_NAME: str
    # DEBUG: bool

    # FrontEnd Application
    FRONTEND_HOST: str

    # JWT Secret Key
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    
    class Config:
        env_file = "env/.env"


class MailSettings(BaseSettings):

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    MAIL_DEBUG: bool
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    USE_CREDENTIALS: bool


    class Config:
        env_file = "env/.env.mail"


settings = Settings()
app_settings = AppSettings()
mail_settings = MailSettings()
