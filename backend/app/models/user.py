from sqlalchemy import Column, Integer, String
from app.core.database import Base

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    citizen_id = Column(String(13), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")

    