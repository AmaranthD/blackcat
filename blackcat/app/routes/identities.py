from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.identity import Identity, IdentityStatus
from app.schemas.identity import (
    IdentityCreate,
    IdentityUpdate,
    IdentityResponse,
    IdentitySimpleResponse,
)

router = APIRouter(prefix="/identities", tags=["identities"])


@router.post("", response_model=IdentitySimpleResponse, status_code=status.HTTP_201_CREATED)
async def create_identity(
    identity_data: IdentityCreate,
    db: Session = Depends(get_db),
):
    """Create a new identity"""
    # Check if identity already exists
    existing = db.query(Identity).filter(
        (Identity.employee_id == identity_data.employee_id) |
        (Identity.username == identity_data.username) |
        (Identity.email == identity_data.email)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Identity with this employee_id, username, or email already exists"
        )
    
    # Create new identity
    new_identity = Identity(
        employee_id=identity_data.employee_id,
        username=identity_data.username,
        email=identity_data.email,
        name=identity_data.name,
        department=identity_data.department,
        job_title=identity_data.job_title,
        status=IdentityStatus.ACTIVE
    )
    
    db.add(new_identity)
    db.commit()
    db.refresh(new_identity)
    
    return IdentitySimpleResponse(
        id=str(new_identity.id),
        username=new_identity.username,
        status=new_identity.status
    )


@router.get("", response_model=List[IdentityResponse])
async def list_identities(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all identities"""
    identities = db.query(Identity).offset(skip).limit(limit).all()
    
    return [
        IdentityResponse(
            id=str(i.id),
            employee_id=i.employee_id,
            username=i.username,
            email=i.email,
            name=i.name,
            department=i.department,
            job_title=i.job_title,
            status=i.status,
            created_at=i.created_at.isoformat(),
            updated_at=i.updated_at.isoformat(),
        )
        for i in identities
    ]


@router.get("/{identity_id}", response_model=IdentityResponse)
async def get_identity(
    identity_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific identity by ID"""
    try:
        uuid_id = UUID(identity_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid identity ID format"
        )
    
    identity = db.query(Identity).filter(Identity.id == uuid_id).first()
    
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity not found"
        )
    
    return IdentityResponse(
        id=str(identity.id),
        employee_id=identity.employee_id,
        username=identity.username,
        email=identity.email,
        name=identity.name,
        department=identity.department,
        job_title=identity.job_title,
        status=identity.status,
        created_at=identity.created_at.isoformat(),
        updated_at=identity.updated_at.isoformat(),
    )


@router.patch("/{identity_id}", response_model=IdentityResponse)
async def update_identity(
    identity_id: str,
    identity_data: IdentityUpdate,
    db: Session = Depends(get_db),
):
    """Update an identity"""
    try:
        uuid_id = UUID(identity_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid identity ID format"
        )
    
    identity = db.query(Identity).filter(Identity.id == uuid_id).first()
    
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity not found"
        )
    
    # Update only provided fields
    update_data = identity_data.model_dump(exclude_unset=True)
    
    # Check if email or username is being changed to an existing value
    if "email" in update_data:
        existing = db.query(Identity).filter(
            (Identity.email == update_data["email"]) & (Identity.id != uuid_id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )
    
    if "username" in update_data:
        existing = db.query(Identity).filter(
            (Identity.username == update_data["username"]) & (Identity.id != uuid_id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already in use"
            )
    
    for key, value in update_data.items():
        setattr(identity, key, value)
    
    db.commit()
    db.refresh(identity)
    
    return IdentityResponse(
        id=str(identity.id),
        employee_id=identity.employee_id,
        username=identity.username,
        email=identity.email,
        name=identity.name,
        department=identity.department,
        job_title=identity.job_title,
        status=identity.status,
        created_at=identity.created_at.isoformat(),
        updated_at=identity.updated_at.isoformat(),
    )


@router.post("/{identity_id}/disable", response_model=IdentityResponse)
async def disable_identity(
    identity_id: str,
    db: Session = Depends(get_db),
):
    """Disable an identity"""
    try:
        uuid_id = UUID(identity_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid identity ID format"
        )
    
    identity = db.query(Identity).filter(Identity.id == uuid_id).first()
    
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity not found"
        )
    
    if identity.status == IdentityStatus.DISABLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identity is already disabled"
        )
    
    identity.status = IdentityStatus.DISABLED
    db.commit()
    db.refresh(identity)
    
    return IdentityResponse(
        id=str(identity.id),
        employee_id=identity.employee_id,
        username=identity.username,
        email=identity.email,
        name=identity.name,
        department=identity.department,
        job_title=identity.job_title,
        status=identity.status,
        created_at=identity.created_at.isoformat(),
        updated_at=identity.updated_at.isoformat(),
    )
