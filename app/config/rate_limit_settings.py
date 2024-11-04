from pydantic_settings import BaseSettings


class RateLimitSettings(BaseSettings):
    DEFAULT_PERIOD: int
    DEFAULT_DEVICE_COOLDOWN: int
    DEFAULT_IP_COOLDOWN: int

    REGISTER_USER_DEVICE_RATE_LIMIT: int
    REGISTER_USER_IP_RATE_LIMIT: int

    VERIFY_USER_ACCOUNT_DEVICE_RATE_LIMIT: int
    VERIFY_USER_ACCOUNT_IP_RATE_LIMIT: int

    LOGIN_USER_DEVICE_RATE_LIMIT: int
    LOGIN_USER_IP_RATE_LIMIT: int

    REFRESH_TOKEN_DEVICE_RATE_LIMIT: int
    REFRESH_TOKEN_IP_RATE_LIMIT: int

    FORGOT_PASSWORD_DEVICE_RATE_LIMIT: int
    FORGOT_PASSWORD_IP_RATE_LIMIT: int

    VERIFY_FORGOT_PASSWORD_DEVICE_RATE_LIMIT: int
    VERIFY_FORGOT_PASSWORD_IP_RATE_LIMIT: int

    RESET_PASSWORD_DEVICE_RATE_LIMIT: int
    RESET_PASSWORD_IP_RATE_LIMIT: int


    class Config:
        # env_file = "env/.env.ratelimiting"
        env_file = "env/.env.ratelimiting"


rate_limit_settings = RateLimitSettings()

# Updated rate limit configuration
RATE_LIMIT_CONFIG = {
    "register_user": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.REGISTER_USER_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.REGISTER_USER_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
    "verify_user_account": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.VERIFY_USER_ACCOUNT_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.VERIFY_USER_ACCOUNT_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
    "login_user": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.LOGIN_USER_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.LOGIN_USER_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
    "refresh_token": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.REFRESH_TOKEN_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.REFRESH_TOKEN_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
    "forgot_password": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.FORGOT_PASSWORD_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.FORGOT_PASSWORD_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
    "verify_forgot_password": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.VERIFY_FORGOT_PASSWORD_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.VERIFY_FORGOT_PASSWORD_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
    "reset_password": {
        "period": rate_limit_settings.DEFAULT_PERIOD,
        "device_limit": rate_limit_settings.RESET_PASSWORD_DEVICE_RATE_LIMIT,
        "ip_limit": rate_limit_settings.RESET_PASSWORD_IP_RATE_LIMIT,
        "device_cooldown": rate_limit_settings.DEFAULT_DEVICE_COOLDOWN,
        "ip_cooldown": rate_limit_settings.DEFAULT_IP_COOLDOWN,
    },
}