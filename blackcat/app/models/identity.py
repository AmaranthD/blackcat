from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from enum import Enum

from app.database import Base


class IdentityStatus(str, Enum):
    """Status enumeration for Identity"""
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"


class Identity(Base):
    """Identity model representing a user in the system"""
    __tablename__ = "identities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    job_title = Column(String(100), nullable=False)
    status = Column(
        SQLEnum(IdentityStatus),
        nullable=False,
        default=IdentityStatus.ACTIVE,
        index=True
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Identity(id={self.id}, employee_id={self.employee_id}, username={self.username})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "employee_id": self.employee_id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "department": self.department,
            "job_title": self.job_title,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
