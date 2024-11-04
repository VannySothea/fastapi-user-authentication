import time
import redis
from fastapi import Request, HTTPException, Header, status
from app.config.rate_limit_settings import RATE_LIMIT_CONFIG
from app.config.lockout_settings import LOCKOUT_CONFIG


async def validate_device_and_apply_rate_limiters(request: Request, operation: str, device_id: str = Header(...)):

    if not device_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device ID is required.")
    
    if not request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to get the IP address")
    
    await apply_device_rate_limiter(device_id=device_id, operation=operation)
    await apply_ip_rate_limiter(request, operation=operation)


# Set up the Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


class RateLimiter:
    def __init__(self, limit: int, period: int, cooldown: int):
        self.limit = limit  # Max number of requests
        self.period = period  # Time window (in seconds)
        self.cooldown = cooldown  # Cooldown duration (in seconds)

    def is_allowed(self, key: str) -> bool:
        current_time = int(time.time())

        try:
            # Check if the cooldown key exists first
            if redis_client.exists(f"cooldown:{key}"):
                ttl = redis_client.ttl(f"cooldown:{key}")
                print(f"Cooldown in effect for {key}. Cooldown expires in {ttl} seconds.")
                return False  # Client is still in cooldown

            # Check the number of requests in the past period
            pipeline = redis_client.pipeline()
            pipeline.zremrangebyscore(key, 0, current_time - self.period)  # Remove old timestamps
            pipeline.zadd(key, {current_time: current_time})  # Add the current timestamp
            pipeline.zcard(key)  # Count the number of timestamps (requests)
            pipeline.expire(key, self.period)  # Set expiration for the key
            result = pipeline.execute()

            count = result[-2]  # zcard result (second last command result)
            print(f"Request count for {key}: {count}, limit: {self.limit}, time: {current_time}")

            if count >= self.limit:
                # Exceeded the rate limit, set a cooldown key and reset the request count
                # redis_client.setex(f"cooldown:{key}", self.cooldown, "1")  # Set cooldown with expiration
                redis_client.setex(f"cooldown:{key}", self.cooldown, "1")  # Set cooldown with expiration
                redis_client.delete(key)  # Reset the request count by deleting the key
                print(f"Rate limit exceeded for {key}. Cooldown activated for {self.cooldown} seconds.")
                return False

            return True
        
        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")
            return False  # Returning False indicates that the request was not allowed due to an error


class Lockout:
    def __init__(self, fail_limit: int, lockout_period: int, cooldown_period: int):
        self.fail_limit = fail_limit  # Maximum allowed failed attempts
        self.lockout_period = lockout_period  # Lockout duration in seconds
        self.cooldown_period = cooldown_period  # Cooldown duration in seconds

    def is_locked_out(self, key: str) -> bool:
        try:
            if redis_client.exists(f"lockout:{key}"):  # Check for the lockout key
                print(f"Lockout active for {key}. Lockout expires in {redis_client.ttl(f'lockout:{key}')} seconds.")
                return True
            return False
        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")
            return False

    def record_failed_attempt(self, key: str) -> None:
        try:
            failed_attempts = redis_client.incr(key)
            print(f"Failed attempt count for {key}: {failed_attempts}")
            
            if failed_attempts == 1:
                redis_client.expire(key, self.cooldown_period)  # Set cooldown expiration for first failed attempt
            
            if failed_attempts >= self.fail_limit:
                print(f"Lockout activated for {key} due to too many failed attempts.")
                redis_client.setex(f"lockout:{key}", self.lockout_period, "1")  # Set lockout key
        except redis.exceptions.RedisError as e:
            print(f"Redis error: {e}")



# Apply rate limiter based on operation
async def apply_ip_rate_limiter(request: Request, operation: str):
    client_ip = request.client.host
    key = f"rate_limit:{operation}:{client_ip}"

    # Use constants from the config file
    rate_limiter = RateLimiter(
        limit=RATE_LIMIT_CONFIG[operation]["ip_limit"],
        period=RATE_LIMIT_CONFIG[operation]["period"],
        cooldown=RATE_LIMIT_CONFIG[operation]["ip_cooldown"]
    )
    
    if not rate_limiter.is_allowed(key):
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded for {operation}. Try again later.")
    
    
async def apply_device_rate_limiter(device_id: str, operation: str):
    key = f"rate_limit:{operation}:{device_id}"

    # Use constants from the config file
    rate_limiter = RateLimiter(
        limit=RATE_LIMIT_CONFIG[operation]["device_limit"],
        period=RATE_LIMIT_CONFIG[operation]["period"],
        cooldown=RATE_LIMIT_CONFIG[operation]["device_cooldown"]
    )
    if not rate_limiter.is_allowed(key):
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded for {operation}. Try again later.")

    
async def record_ip_lockout_attempt(request: Request, operation: str):
    client_ip = request.client.host
    key = f"lockout:{operation}:{client_ip}"
    lockout = Lockout(
        fail_limit=LOCKOUT_CONFIG[operation]["ip_fail_limit"],
        cooldown_period=LOCKOUT_CONFIG[operation]["cooldown_period"],
        lockout_period=LOCKOUT_CONFIG[operation]["ip_lockout_period"]
    )

    # Record the failed attempt
    lockout.record_failed_attempt(key)


async def record_device_lockout_attempt(device_id: str, operation: str):
    """Helper function to record a failed attempt and apply lockout."""
    key = f"lockout:{operation}:{device_id}"
    # Get lockout settings for the specific operation
    lockout = Lockout(
        fail_limit=LOCKOUT_CONFIG[operation]["device_fail_limit"],
        cooldown_period=LOCKOUT_CONFIG[operation]["cooldown_period"],
        lockout_period=LOCKOUT_CONFIG[operation]["device_lockout_period"]
    )
    # Record the failed attempt
    lockout.record_failed_attempt(key)
    
    
async def apply_ip_lockout(request: Request, operation: str):
    client_ip = request.client.host
    key = f"lockout:{operation}:{client_ip}"
    lockout = Lockout(
        fail_limit=LOCKOUT_CONFIG[operation]["ip_fail_limit"],
        cooldown_period=LOCKOUT_CONFIG[operation]["cooldown_period"],
        lockout_period=LOCKOUT_CONFIG[operation]["ip_lockout_period"]
    )

    if lockout.is_locked_out(key):
        raise HTTPException(status_code=403, detail=f"Too many attempts for {operation}. Try again later.")


async def apply_device_lockout(device_id: str, operation: str):
    key = f"lockout:{operation}:{device_id}"

    lockout = Lockout(
        fail_limit=LOCKOUT_CONFIG[operation]["device_fail_limit"],
        cooldown_period=LOCKOUT_CONFIG[operation]["cooldown_period"],
        lockout_period=LOCKOUT_CONFIG[operation]["device_lockout_period"]
    )

    if lockout.is_locked_out(key):
        raise HTTPException(status_code=403, detail=f"Too many attempts for {operation}. Try again later.")
