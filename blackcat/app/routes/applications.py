from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.application import Application
from app.models.application_entitlement import ApplicationEntitlement
from app.schemas.applications import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationWithEntitlements,
    ApplicationEntitlementCreate,
    ApplicationEntitlementResponse,
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    app_data: ApplicationCreate,
    db: Session = Depends(get_db),
):
    """Create a new application"""
    # Check if application already exists
    existing = db.query(Application).filter(
        Application.name == app_data.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Application with this name already exists"
        )
    
    # Create new application
    new_app = Application(
        name=app_data.name,
        description=app_data.description
    )
    
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    
    return ApplicationResponse(
        id=str(new_app.id),
        name=new_app.name,
        description=new_app.description,
        created_at=new_app.created_at.isoformat(),
        updated_at=new_app.updated_at.isoformat(),
    )


@router.get("", response_model=List[ApplicationWithEntitlements])
async def list_applications(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all applications with their entitlements"""
    applications = db.query(Application).offset(skip).limit(limit).all()
    
    result = []
    for app in applications:
        entitlements = [
            ApplicationEntitlementResponse(
                id=str(e.id),
                application_id=str(e.application_id),
                name=e.name,
                description=e.description,
                created_at=e.created_at.isoformat(),
                updated_at=e.updated_at.isoformat(),
            )
            for e in app.entitlements
        ]
        
        result.append(
            ApplicationWithEntitlements(
                id=str(app.id),
                name=app.name,
                description=app.description,
                entitlements=entitlements,
                created_at=app.created_at.isoformat(),
                updated_at=app.updated_at.isoformat(),
            )
        )
    
    return result


@router.get("/{app_id}", response_model=ApplicationWithEntitlements)
async def get_application(
    app_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific application with its entitlements"""
    try:
        uuid_id = UUID(app_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid application ID format"
        )
    
    app = db.query(Application).filter(Application.id == uuid_id).first()
    
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    entitlements = [
        ApplicationEntitlementResponse(
            id=str(e.id),
            application_id=str(e.application_id),
            name=e.name,
            description=e.description,
            created_at=e.created_at.isoformat(),
            updated_at=e.updated_at.isoformat(),
        )
        for e in app.entitlements
    ]
    
    return ApplicationWithEntitlements(
        id=str(app.id),
        name=app.name,
        description=app.description,
        entitlements=entitlements,
        created_at=app.created_at.isoformat(),
        updated_at=app.updated_at.isoformat(),
    )
