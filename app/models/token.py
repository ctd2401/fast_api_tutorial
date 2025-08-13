from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    client_ip = Column(String, nullable=True)  # Optional field to store client IP
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    expires_at = Column(DateTime)