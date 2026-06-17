"""User model for authentication."""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
import uuid

from app.database import Base


class User(Base):
    """Application user with credentials."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
