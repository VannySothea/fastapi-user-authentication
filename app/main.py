from fastapi import FastAPI
from app.routes import user, security
from app.jobs.scheduler import start_scheduler, shutdown_scheduler
from app.config.role import initialize_app_roles
initialize_app_roles()




def create_application():
    application = FastAPI()

    # User
    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
    application.include_router(user.business_router)
    application.include_router(user.admin_router)

    # Security
    application.include_router(security.auth_router)
    return application


app = create_application()

@app.get("/")
async def root():
    return "This is in main page"


# Start the scheduler
start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    shutdown_scheduler()

