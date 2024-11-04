from sqlalchemy.orm import Session
from app.models.user import Role
from app.config.database import SessionLocal
from sqlalchemy.future import select

# Function or main entry point where roles are initialized
def initialize_app_roles():
    # Create a session
    session = SessionLocal()  # Create a new session using your SessionLocal (SQLAlchemy session factory)
    
    try:
        # def delete_existing_role(session: Session):
        #     print("Trying to delete existing role")
        #     existing_roles = session.query(Role).all()
        #     for role in existing_roles:
        #         session.delete(role)
        #     session.commit()

        def initialize_roles(session: Session):
            print("Generating role")
            roles = ["normal_user", "education_user", "business_user", "admin"]
            for role_name in roles:
                role = session.query(Role).filter_by(role_name=role_name).first()

                if not role:
                    new_role = Role(role_name=role_name)
                    session.add(new_role)

            session.commit()
        # delete_existing_role(session)
        initialize_roles(session)
    finally:
        # Close the session after you're done
        session.close()

# # Call the function where needed in the code (e.g., when starting the application)
# initialize_app_roles()

async def normal_user(session):
    normal_user = await session.execute(
        select(Role).filter_by(role_name='normal_user')
    )
    return normal_user.scalar_one_or_none()  # Returns the Role object or None if not found

async def education_user(session):
    education_user = await session.execute(
        select(Role).filter_by(role_name='education_user')
    )
    return education_user.scalar_one_or_none()  # Returns the Role object or None if not found

async def business_user(session):
    business_user = await session.execute(
        select(Role).filter_by(role_name='business_user')
    )
    return business_user.scalar_one_or_none()  # Returns the Role object or None if not found

async def admin(session):
    admin = await session.execute(
        select(Role).filter_by(role_name='admin')
    )
    return admin.scalar_one_or_none()  # Returns the Role object or None if not found
