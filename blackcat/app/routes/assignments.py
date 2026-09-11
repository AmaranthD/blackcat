from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.identity import Identity
from app.models.application_entitlement import ApplicationEntitlement
from app.models.assignment import Assignment, AssignmentStatus, AssignmentSource
from app.schemas.assignments import (
    AssignmentCreate,
    AssignmentResponse,
    AssignmentWithDetails,
)

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
):
    """Create a new assignment (grant entitlement to identity)"""
    try:
        identity_uuid = UUID(assignment_data.identity_id)
        entitlement_uuid = UUID(assignment_data.entitlement_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format for identity_id or entitlement_id"
        )
    
    # Check if identity exists
    identity = db.query(Identity).filter(Identity.id == identity_uuid).first()
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity not found"
        )
    
    # Check if entitlement exists
    entitlement = db.query(ApplicationEntitlement).filter(
        ApplicationEntitlement.id == entitlement_uuid
    ).first()
    if not entitlement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entitlement not found"
        )
    
    # Check if assignment already exists (active or revoked)
    existing = db.query(Assignment).filter(
        (Assignment.identity_id == identity_uuid) &
        (Assignment.entitlement_id == entitlement_uuid) &
        (Assignment.status != AssignmentStatus.REVOKED)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Identity already has this entitlement assigned"
        )
    
    # Create new assignment
    new_assignment = Assignment(
        identity_id=identity_uuid,
        entitlement_id=entitlement_uuid,
        source=assignment_data.source,
        expires_at=assignment_data.expires_at,
        status=AssignmentStatus.ACTIVE
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return AssignmentResponse(
        id=str(new_assignment.id),
        identity_id=str(new_assignment.identity_id),
        entitlement_id=str(new_assignment.entitlement_id),
        status=new_assignment.status,
        source=new_assignment.source,
        created_at=new_assignment.created_at.isoformat(),
        expires_at=new_assignment.expires_at.isoformat() if new_assignment.expires_at else None,
        updated_at=new_assignment.updated_at.isoformat(),
    )


@router.get("", response_model=List[AssignmentWithDetails])
async def list_assignments(
    db: Session = Depends(get_db),
    identity_id: str = None,
    entitlement_id: str = None,
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100,
):
    """List assignments with optional filters"""
    query = db.query(Assignment)
    
    if identity_id:
        try:
            identity_uuid = UUID(identity_id)
            query = query.filter(Assignment.identity_id == identity_uuid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid identity_id format"
            )
    
    if entitlement_id:
        try:
            entitlement_uuid = UUID(entitlement_id)
            query = query.filter(Assignment.entitlement_id == entitlement_uuid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid entitlement_id format"
            )
    
    if status_filter:
        try:
            status_enum = AssignmentStatus(status_filter)
            query = query.filter(Assignment.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join([s.value for s in AssignmentStatus])}"
            )
    
    assignments = query.offset(skip).limit(limit).all()
    
    result = []
    for assignment in assignments:
        identity_dict = {
            "id": str(assignment.identity.id),
            "username": assignment.identity.username,
            "email": assignment.identity.email,
            "name": assignment.identity.name,
        }
        
        entitlement_dict = {
            "id": str(assignment.entitlement.id),
            "name": assignment.entitlement.name,
            "description": assignment.entitlement.description,
            "application": {
                "id": str(assignment.entitlement.application.id),
                "name": assignment.entitlement.application.name,
            }
        }
        
        result.append(
            AssignmentWithDetails(
                id=str(assignment.id),
                identity=identity_dict,
                entitlement=entitlement_dict,
                status=assignment.status,
                source=assignment.source,
                created_at=assignment.created_at.isoformat(),
                expires_at=assignment.expires_at.isoformat() if assignment.expires_at else None,
                updated_at=assignment.updated_at.isoformat(),
            )
        )
    
    return result


@router.get("/{identity_id}/entitlements", response_model=List[AssignmentWithDetails])
async def get_identity_entitlements(
    identity_id: str,
    db: Session = Depends(get_db),
    active_only: bool = True,
):
    """Get all entitlements assigned to an identity"""
    try:
        identity_uuid = UUID(identity_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid identity_id format"
        )
    
    # Check if identity exists
    identity = db.query(Identity).filter(Identity.id == identity_uuid).first()
    if not identity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Identity not found"
        )
    
    query = db.query(Assignment).filter(Assignment.identity_id == identity_uuid)
    
    if active_only:
        query = query.filter(Assignment.status == AssignmentStatus.ACTIVE)
    
    assignments = query.all()
    
    result = []
    for assignment in assignments:
        identity_dict = {
            "id": str(assignment.identity.id),
            "username": assignment.identity.username,
            "email": assignment.identity.email,
            "name": assignment.identity.name,
        }
        
        entitlement_dict = {
            "id": str(assignment.entitlement.id),
            "name": assignment.entitlement.name,
            "description": assignment.entitlement.description,
            "application": {
                "id": str(assignment.entitlement.application.id),
                "name": assignment.entitlement.application.name,
            }
        }
        
        result.append(
            AssignmentWithDetails(
                id=str(assignment.id),
                identity=identity_dict,
                entitlement=entitlement_dict,
                status=assignment.status,
                source=assignment.source,
                created_at=assignment.created_at.isoformat(),
                expires_at=assignment.expires_at.isoformat() if assignment.expires_at else None,
                updated_at=assignment.updated_at.isoformat(),
            )
        )
    
    return result


@router.post("/{assignment_id}/revoke", response_model=AssignmentResponse)
async def revoke_assignment(
    assignment_id: str,
    db: Session = Depends(get_db),
):
    """Revoke an assignment"""
    try:
        uuid_id = UUID(assignment_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assignment ID format"
        )
    
    assignment = db.query(Assignment).filter(Assignment.id == uuid_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    if assignment.status == AssignmentStatus.REVOKED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment is already revoked"
        )
    
    assignment.status = AssignmentStatus.REVOKED
    db.commit()
    db.refresh(assignment)
    
    return AssignmentResponse(
        id=str(assignment.id),
        identity_id=str(assignment.identity_id),
        entitlement_id=str(assignment.entitlement_id),
        status=assignment.status,
        source=assignment.source,
        created_at=assignment.created_at.isoformat(),
        expires_at=assignment.expires_at.isoformat() if assignment.expires_at else None,
        updated_at=assignment.updated_at.isoformat(),
    )


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific assignment by ID"""
    try:
        uuid_id = UUID(assignment_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assignment ID format"
        )
    
    assignment = db.query(Assignment).filter(Assignment.id == uuid_id).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return AssignmentResponse(
        id=str(assignment.id),
        identity_id=str(assignment.identity_id),
        entitlement_id=str(assignment.entitlement_id),
        status=assignment.status,
        source=assignment.source,
        created_at=assignment.created_at.isoformat(),
        expires_at=assignment.expires_at.isoformat() if assignment.expires_at else None,
        updated_at=assignment.updated_at.isoformat(),
    )
