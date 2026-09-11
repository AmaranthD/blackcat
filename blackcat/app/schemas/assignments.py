from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class AssignmentStatus(str, Enum):
    """Status enumeration"""
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class AssignmentSource(str, Enum):
    """Source enumeration"""
    MANUAL = "MANUAL"
    POLICY = "POLICY"
    IMPORT = "IMPORT"


class AssignmentCreate(BaseModel):
    """Schema for creating an assignment"""
    identity_id: str = Field(..., description="UUID of the identity")
    entitlement_id: str = Field(..., description="UUID of the entitlement")
    source: AssignmentSource = Field(default=AssignmentSource.MANUAL)
    expires_at: Optional[datetime] = Field(None, description="Optional expiration date")

    class Config:
        json_schema_extra = {
            "example": {
                "identity_id": "uuid-of-juan",
                "entitlement_id": "uuid-of-github-developer",
                "source": "MANUAL",
                "expires_at": "2025-12-31T23:59:59"
            }
        }


class AssignmentResponse(BaseModel):
    """Schema for assignment response"""
    id: str
    identity_id: str
    entitlement_id: str
    status: AssignmentStatus
    source: AssignmentSource
    created_at: str
    expires_at: Optional[str]
    updated_at: str

    class Config:
        from_attributes = True


class AssignmentWithDetails(BaseModel):
    """Schema for assignment response with identity and entitlement details"""
    id: str
    identity: dict  # Identity details
    entitlement: dict  # Entitlement details with application info
    status: AssignmentStatus
    source: AssignmentSource
    created_at: str
    expires_at: Optional[str]
    updated_at: str

    class Config:
        from_attributes = True
