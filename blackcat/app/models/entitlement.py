from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database import Base


class Entitlement(Base):
    """Entitlement model representing permissions/roles for an Identity"""
    __tablename__ = "entitlements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identity_id = Column(UUID(as_uuid=True), ForeignKey("identities.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Identity
    identity = relationship("Identity", backref="entitlements")

    def __repr__(self):
        return f"<Entitlement(id={self.id}, identity_id={self.identity_id}, name={self.name})>"

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "identity_id": str(self.identity_id),
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
