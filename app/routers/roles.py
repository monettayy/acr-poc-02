from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=schemas.RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """Create a new role"""
    # Check if role with name already exists
    existing_role = crud.get_role_by_name(db, name=role.name)
    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Role with this name already exists"
        )
    
    return crud.create_role(db=db, role=role)


@router.get("/", response_model=List[schemas.RoleResponse])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all roles with pagination"""
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles


@router.get("/{role_id}", response_model=schemas.RoleResponse)
def read_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role by ID"""
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.put("/{role_id}", response_model=schemas.RoleResponse)
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db)):
    """Update a role (except Superuser)"""
    # Check if role exists
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Check if trying to update Superuser role
    if db_role.name == "Superuser":
        raise HTTPException(
            status_code=403,
            detail="Cannot update Superuser role"
        )
    
    # Check if new name conflicts with existing role
    if role_update.name and role_update.name != db_role.name:
        existing_role = crud.get_role_by_name(db, name=role_update.name)
        if existing_role:
            raise HTTPException(
                status_code=400,
                detail="Role with this name already exists"
            )
    
    updated_role = crud.update_role(db=db, role_id=role_id, role_update=role_update)
    if updated_role is None:
        raise HTTPException(
            status_code=403,
            detail="Cannot update Superuser role"
        )
    return updated_role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role (except Superuser)"""
    # Check if role exists
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Check if trying to delete Superuser role
    if db_role.name == "Superuser":
        raise HTTPException(
            status_code=403,
            detail="Cannot delete Superuser role"
        )
    
    success = crud.delete_role(db=db, role_id=role_id)
    if not success:
        raise HTTPException(
            status_code=403,
            detail="Cannot delete Superuser role"
        )
    return None
