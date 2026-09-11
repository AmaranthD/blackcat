from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.application import Application
from app.models.application_entitlement import ApplicationEntitlement
from app.schemas.applications import (
    ApplicationEntitlementCreate,
    ApplicationEntitlementResponse,
)

router = APIRouter(tags=["entitlements"])


@router.post("/applications/{application_id}/entitlements", response_model=ApplicationEntitlementResponse, status_code=status.HTTP_201_CREATED)
async def create_entitlement(
    application_id: str,
    entitlement_data: ApplicationEntitlementCreate,
    db: Session = Depends(get_db),
):
    """Create a new entitlement for an application"""
    try:
        app_uuid = UUID(application_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid application ID format"
        )
    
    # Check if application exists
    app = db.query(Application).filter(Application.id == app_uuid).first()
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Check if entitlement already exists for this application
    existing = db.query(ApplicationEntitlement).filter(
        (ApplicationEntitlement.application_id == app_uuid) &
        (ApplicationEntitlement.name == entitlement_data.name)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Entitlement with this name already exists for this application"
        )
    
    # Create new entitlement
    new_entitlement = ApplicationEntitlement(
        application_id=app_uuid,
        name=entitlement_data.name,
        description=entitlement_data.description
    )
    
    db.add(new_entitlement)
    db.commit()
    db.refresh(new_entitlement)
    
    return ApplicationEntitlementResponse(
        id=str(new_entitlement.id),
        application_id=str(new_entitlement.application_id),
        name=new_entitlement.name,
        description=new_entitlement.description,
        created_at=new_entitlement.created_at.isoformat(),
        updated_at=new_entitlement.updated_at.isoformat(),
    )


@router.get("/entitlements", response_model=List[ApplicationEntitlementResponse])
async def list_all_entitlements(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all entitlements from all applications"""
    entitlements = db.query(ApplicationEntitlement).offset(skip).limit(limit).all()
    
    return [
        ApplicationEntitlementResponse(
            id=str(e.id),
            application_id=str(e.application_id),
            name=e.name,
            description=e.description,
            created_at=e.created_at.isoformat(),
            updated_at=e.updated_at.isoformat(),
        )
        for e in entitlements
    ]


@router.get("/applications/{application_id}/entitlements", response_model=List[ApplicationEntitlementResponse])
async def list_application_entitlements(
    application_id: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List entitlements for a specific application"""
    try:
        app_uuid = UUID(application_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid application ID format"
        )
    
    # Check if application exists
    app = db.query(Application).filter(Application.id == app_uuid).first()
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    entitlements = db.query(ApplicationEntitlement).filter(
        ApplicationEntitlement.application_id == app_uuid
    ).offset(skip).limit(limit).all()
    
    return [
        ApplicationEntitlementResponse(
            id=str(e.id),
            application_id=str(e.application_id),
            name=e.name,
            description=e.description,
            created_at=e.created_at.isoformat(),
            updated_at=e.updated_at.isoformat(),
        )
        for e in entitlements
    ]


@router.get("/entitlements/{entitlement_id}", response_model=ApplicationEntitlementResponse)
async def get_entitlement(
    entitlement_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific entitlement by ID"""
    try:
        uuid_id = UUID(entitlement_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid entitlement ID format"
        )
    
    entitlement = db.query(ApplicationEntitlement).filter(
        ApplicationEntitlement.id == uuid_id
    ).first()
    
    if not entitlement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entitlement not found"
        )
    
    return ApplicationEntitlementResponse(
        id=str(entitlement.id),
        application_id=str(entitlement.application_id),
        name=entitlement.name,
        description=entitlement.description,
        created_at=entitlement.created_at.isoformat(),
        updated_at=entitlement.updated_at.isoformat(),
    )
