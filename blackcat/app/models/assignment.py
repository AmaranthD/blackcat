from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from enum import Enum

from app.database import Base


class AssignmentStatus(str, Enum):
    """Status enumeration for Assignment"""
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class AssignmentSource(str, Enum):
    """Source enumeration for Assignment"""
    MANUAL = "MANUAL"          # Administrator manually assigned
    POLICY = "POLICY"          # Assigned by a policy engine
    IMPORT = "IMPORT"          # Imported from external system


class Assignment(Base):
    """Assignment model linking Identity to ApplicationEntitlement"""
    __tablename__ = "assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False, index=True)
    entitlement_id = Column(UUID(as_uuid=True), ForeignKey("application_entitlements.id"), nullable=False, index=True)
    status = Column(
        SQLEnum(AssignmentStatus),
        nullable=False,
        default=AssignmentStatus.ACTIVE,
        index=True
    )
    source = Column(
        SQLEnum(AssignmentSource),
        nullable=False,
        default=AssignmentSource.MANUAL,
        index=True
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    identity = relationship("Identity", backref="assignments")
    entitlement = relationship("ApplicationEntitlement", backref="assignments")

    def __repr__(self):
        return f"<Assignment(id={self.id}, identity_id={self.identity_id}, entitlement_id={self.entitlement_id})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "identity_id": str(self.identity_id),
            "entitlement_id": str(self.entitlement_id),
            "status": self.status.value,
            "source": self.source.value,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "updated_at": self.updated_at.isoformat(),
        }
