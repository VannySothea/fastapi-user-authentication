from app.config.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, text, Table
from sqlalchemy.orm import relationship, mapped_column


class VerificationCodeOpt(Base):
    __tablename__ = "verification_codes_opt"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('registration_requests.user_id', ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)

    user = relationship("RegistrationRequest", back_populates="verification_code")


class RegistrationRequest(Base):
    __tablename__ = 'registration_requests'
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    verification_code = relationship("VerificationCodeOpt", back_populates="user")


class VerificationCode(Base):
    __tablename__ = "verification_codes"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)

    user = relationship("User", back_populates="verification_code")


class Code(Base):
    __tablename__ = "codes"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)

    user = relationship("User", back_populates="code")


# Many-to-Many relationship between Users and Roles
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete="CASCADE")),
    Column('role_id', Integer, ForeignKey('roles.role_id', ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    user_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    status = Column(String, server_default=text("'active'"), nullable=False)
    verified_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'), nullable=False)


    # Defines a many to many relationship between role
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    tokens = relationship("UserToken", back_populates="user")
    verification_code = relationship("VerificationCode", back_populates="user")
    code = relationship("Code", back_populates="user")


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    role_name = Column(String(50), unique=True, nullable=False)

    # Defines a many to many relationship between user
    users = relationship("User", secondary=user_roles, back_populates="roles")
    

class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False, index=True)
    access_key = Column(String(250), nullable=False, index=True)
    refresh_key = Column(String(250), nullable=False, index=True)
    device_id = Column(String, nullable=False, index=True)
    device_name = Column(String, nullable=False, server_default=text("'NONAME'"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    last_used_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    
    user = relationship("User", back_populates="tokens")
