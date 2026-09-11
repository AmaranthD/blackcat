from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class IdentityStatus(str, Enum):
    """Status enumeration"""
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"


class IdentityCreate(BaseModel):
    """Schema for creating an identity"""
    employee_id: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    department: str = Field(..., min_length=1, max_length=100)
    job_title: str = Field(..., min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "10001",
                "username": "juan",
                "email": "juan@example.com",
                "name": "Juan",
                "department": "engineering",
                "job_title": "software-engineer"
            }
        }


class IdentityUpdate(BaseModel):
    """Schema for updating an identity"""
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    job_title: Optional[str] = Field(None, min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Juan Updated",
                "job_title": "senior-engineer"
            }
        }


class IdentityResponse(BaseModel):
    """Schema for identity response"""
    id: str
    employee_id: str
    username: str
    email: str
    name: str
    department: str
    job_title: str
    status: IdentityStatus
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class IdentitySimpleResponse(BaseModel):
    """Schema for simple identity response (POST creation)"""
    id: str
    username: str
    status: IdentityStatus

    class Config:
        from_attributes = True
