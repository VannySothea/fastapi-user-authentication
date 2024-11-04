from pydantic_settings import BaseSettings


class LockoutSettings(BaseSettings):
    DEFAULT_COOLDOWN_PERIOD: int

    CREATE_USER_ACCOUNT_DEVICE_FAIL_LIMIT: int
    CREATE_USER_ACCOUNT_DEVICE_LOCKOUT_PERIOD: int
    CREATE_USER_ACCOUNT_IP_FAIL_LIMIT: int
    CREATE_USER_ACCOUNT_IP_LOCKOUT_PERIOD: int

    ACTIVATE_USER_ACCOUNT_COOLDOWN_PERIOD: int
    ACTIVATE_USER_ACCOUNT_DEVICE_FAIL_LIMIT: int
    ACTIVATE_USER_ACCOUNT_DEVICE_LOCKOUT_PERIOD: int
    ACTIVATE_USER_ACCOUNT_IP_FAIL_LIMIT: int
    ACTIVATE_USER_ACCOUNT_IP_LOCKOUT_PERIOD: int

    GET_LOGIN_TOKEN_COOLDOWN_PERIOD: int
    GET_LOGIN_TOKEN_DEVICE_FAIL_LIMIT: int
    GET_LOGIN_TOKEN_DEVICE_LOCKOUT_PERIOD: int
    GET_LOGIN_TOKEN_IP_FAIL_LIMIT: int
    GET_LOGIN_TOKEN_IP_LOCKOUT_PERIOD: int

    GET_REFRESH_TOKEN_DEVICE_FAIL_LIMIT: int
    GET_REFRESH_TOKEN_DEVICE_LOCKOUT_PERIOD: int
    GET_REFRESH_TOKEN_IP_FAIL_LIMIT: int
    GET_REFRESH_TOKEN_IP_LOCKOUT_PERIOD: int
    
    EMAIL_FORGOT_PASSWORD_LINK_DEVICE_FAIL_LIMIT: int
    EMAIL_FORGOT_PASSWORD_LINK_DEVICE_LOCKOUT_PERIOD: int
    EMAIL_FORGOT_PASSWORD_LINK_IP_FAIL_LIMIT: int
    EMAIL_FORGOT_PASSWORD_LINK_IP_LOCKOUT_PERIOD: int
    
    VERIFY_FORGOT_USER_PASSWORD_COOLDOWN_PERIOD: int
    VERIFY_FORGOT_USER_PASSWORD_DEVICE_FAIL_LIMIT: int
    VERIFY_FORGOT_USER_PASSWORD_DEVICE_LOCKOUT_PERIOD: int
    VERIFY_FORGOT_USER_PASSWORD_IP_FAIL_LIMIT: int
    VERIFY_FORGOT_USER_PASSWORD_IP_LOCKOUT_PERIOD: int
    
    RESET_USER_PASSWORD_COOLDOWN_PERIOD: int
    RESET_USER_PASSWORD_DEVICE_FAIL_LIMIT: int
    RESET_USER_PASSWORD_DEVICE_LOCKOUT_PERIOD: int
    RESET_USER_PASSWORD_IP_FAIL_LIMIT: int
    RESET_USER_PASSWORD_IP_LOCKOUT_PERIOD: int

        
    class Config:
        # env_file = "env/.env.lockout"
        env_file = "env/.env.lockout"


lockout_settings = LockoutSettings()

# Lockout Configurations
LOCKOUT_CONFIG = {
    "create_user_account": {
        "cooldown_period": lockout_settings.DEFAULT_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.CREATE_USER_ACCOUNT_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.CREATE_USER_ACCOUNT_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.CREATE_USER_ACCOUNT_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.CREATE_USER_ACCOUNT_IP_LOCKOUT_PERIOD,
    },
    "activate_user_account": {
        "cooldown_period": lockout_settings.ACTIVATE_USER_ACCOUNT_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.ACTIVATE_USER_ACCOUNT_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.ACTIVATE_USER_ACCOUNT_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.ACTIVATE_USER_ACCOUNT_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.ACTIVATE_USER_ACCOUNT_IP_LOCKOUT_PERIOD,
    },
    "get_login_token": {
        "cooldown_period": lockout_settings.GET_LOGIN_TOKEN_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.GET_LOGIN_TOKEN_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.GET_LOGIN_TOKEN_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.GET_LOGIN_TOKEN_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.GET_LOGIN_TOKEN_IP_LOCKOUT_PERIOD,
    },
    "get_refresh_token": {
        "cooldown_period": lockout_settings.DEFAULT_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.GET_REFRESH_TOKEN_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.GET_REFRESH_TOKEN_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.GET_REFRESH_TOKEN_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.GET_REFRESH_TOKEN_IP_LOCKOUT_PERIOD,
    },
    "email_forgot_password_link": {
        "cooldown_period": lockout_settings.DEFAULT_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.EMAIL_FORGOT_PASSWORD_LINK_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.EMAIL_FORGOT_PASSWORD_LINK_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.EMAIL_FORGOT_PASSWORD_LINK_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.EMAIL_FORGOT_PASSWORD_LINK_IP_LOCKOUT_PERIOD,
    },
    "verify_forgot_user_password": {
        "cooldown_period": lockout_settings.VERIFY_FORGOT_USER_PASSWORD_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.VERIFY_FORGOT_USER_PASSWORD_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.VERIFY_FORGOT_USER_PASSWORD_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.VERIFY_FORGOT_USER_PASSWORD_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.VERIFY_FORGOT_USER_PASSWORD_IP_LOCKOUT_PERIOD,
    },
    "reset_user_password": {
        "cooldown_period": lockout_settings.RESET_USER_PASSWORD_COOLDOWN_PERIOD,
        "device_fail_limit": lockout_settings.RESET_USER_PASSWORD_DEVICE_FAIL_LIMIT,
        "device_lockout_period": lockout_settings.RESET_USER_PASSWORD_DEVICE_LOCKOUT_PERIOD,
        "ip_fail_limit": lockout_settings.RESET_USER_PASSWORD_IP_FAIL_LIMIT,
        "ip_lockout_period": lockout_settings.RESET_USER_PASSWORD_IP_LOCKOUT_PERIOD,
    },
}