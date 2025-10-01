from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.utils import hash_password
from typing import List, Optional


# Role CRUD operations
def get_role(db: Session, role_id: int) -> Optional[models.Role]:
    """Get a role by ID"""
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_role_by_name(db: Session, name: str) -> Optional[models.Role]:
    """Get a role by name"""
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Role]:
    """Get all roles with pagination"""
    return db.query(models.Role).offset(skip).limit(limit).all()


def create_role(db: Session, role: schemas.RoleCreate) -> models.Role:
    """Create a new role"""
    db_role = models.Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role_update: schemas.RoleUpdate) -> Optional[models.Role]:
    """Update a role (except Superuser)"""
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    
    # Prevent updating Superuser role
    if db_role.name == "Superuser":
        return None
    
    update_data = role_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_role, field, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int) -> bool:
    """Delete a role (except Superuser)"""
    db_role = get_role(db, role_id)
    if not db_role:
        return False
    
    # Prevent deleting Superuser role
    if db_role.name == "Superuser":
        return False
    
    db.delete(db_role)
    db.commit()
    return True


# User CRUD operations
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get a user by ID with role information"""
    return db.query(models.User).options(joinedload(models.User.role)).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users with pagination and role information"""
    return db.query(models.User).options(joinedload(models.User.role)).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    # Hash password if provided
    password_hash = None
    if user.password:
        password_hash = hash_password(user.password)
    
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        role_id=user.role_id,
        password_hash=password_hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


# Default data creation functions
def create_default_roles(db: Session) -> None:
    """Create default roles if they don't exist"""
    # Create Superuser role
    superuser_role = get_role_by_name(db, "Superuser")
    if not superuser_role:
        superuser_role = models.Role(name="Superuser")
        db.add(superuser_role)
    
    # Create User role
    user_role = get_role_by_name(db, "User")
    if not user_role:
        user_role = models.Role(name="User")
        db.add(user_role)
    
    db.commit()


def create_default_superuser(db: Session) -> None:
    """Create default superuser if it doesn't exist"""
    # Check if superuser already exists
    existing_admin = get_user_by_username(db, "admin")
    if existing_admin:
        return
    
    # Get Superuser role
    superuser_role = get_role_by_name(db, "Superuser")
    if not superuser_role:
        return
    
    # Create admin user
    admin_user = models.User(
        email="admin@example.com",
        username="admin",
        full_name="Administrator",
        is_active=True,
        role_id=superuser_role.id,
        password_hash=hash_password("admin123")
    )
    db.add(admin_user)
    db.commit()
