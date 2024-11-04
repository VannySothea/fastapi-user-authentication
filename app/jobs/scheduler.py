from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.jobs.cleanup import (
    cleanup_expired_user_registration_request,
    cleanup_expired_user_tokens,
    cleanup_expired_verification_codes_opt,
    cleanup_expired_verification_codes,
    cleanup_expired_codes
)

# Initialize the scheduler
scheduler = AsyncIOScheduler()


# Schedule the cleanup last 24H user registration requests job
scheduler.add_job(cleanup_expired_user_registration_request, 'interval', hours=24)

# Schedule the cleanup expired user tokens job
scheduler.add_job(cleanup_expired_user_tokens, 'interval', hours=24)

# Schedule the cleanup job to cleanup_verification_codes jobs
scheduler.add_job(cleanup_expired_verification_codes_opt, 'interval', hours=24)
scheduler.add_job(cleanup_expired_verification_codes, 'interval', hours=24)
scheduler.add_job(cleanup_expired_codes, 'interval', hours=24)


def start_scheduler():
    """Starts the scheduler."""
    scheduler.start()
    
def shutdown_scheduler():
    """Shuts down the scheduler."""
    scheduler.shutdown()
