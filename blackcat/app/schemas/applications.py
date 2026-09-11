from pydantic import BaseModel, Field
from typing import Optional, List


class ApplicationEntitlementCreate(BaseModel):
    """Schema for creating an application entitlement"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "developer",
                "description": "Developer access level"
            }
        }


class ApplicationEntitlementResponse(BaseModel):
    """Schema for application entitlement response"""
    id: str
    application_id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    """Schema for creating an application"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Github",
                "description": "GitHub repository access management"
            }
        }


class ApplicationResponse(BaseModel):
    """Schema for application response"""
    id: str
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ApplicationWithEntitlements(BaseModel):
    """Schema for application response with entitlements"""
    id: str
    name: str
    description: Optional[str]
    entitlements: List[ApplicationEntitlementResponse] = []
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
