import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models import User, Role
from app import crud

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        # Create default roles for testing
        crud.create_default_roles(db)
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def sample_role_data():
    return {
        "name": "TestRole"
    }


def test_create_role(sample_role_data):
    """Test creating a new role"""
    response = client.post("/roles/", json=sample_role_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_role_data["name"]
    assert "id" in data
    assert "created_at" in data


def test_get_roles():
    """Test getting all roles"""
    response = client.get("/roles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Should have at least Superuser and User roles
    assert len(response.json()) >= 2


def test_get_role():
    """Test getting a specific role"""
    response = client.get("/roles/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_get_role_not_found():
    """Test getting a non-existent role"""
    response = client.get("/roles/999")
    assert response.status_code == 404


def test_create_role_duplicate_name(sample_role_data):
    """Test creating a role with duplicate name"""
    # Create first role
    client.post("/roles/", json=sample_role_data)
    
    # Try to create another role with same name
    response = client.post("/roles/", json=sample_role_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_role():
    """Test updating a role"""
    # Create a test role first
    create_response = client.post("/roles/", json={"name": "UpdateTestRole"})
    role_id = create_response.json()["id"]
    
    # Update the role
    update_data = {"name": "UpdatedRoleName"}
    response = client.put(f"/roles/{role_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "UpdatedRoleName"


def test_update_superuser_role():
    """Test that Superuser role cannot be updated"""
    # Assuming Superuser role has ID 1
    update_data = {"name": "NewSuperuserName"}
    response = client.put("/roles/1", json=update_data)
    assert response.status_code == 403
    assert "Cannot update Superuser role" in response.json()["detail"]


def test_delete_role():
    """Test deleting a role"""
    # Create a test role first
    create_response = client.post("/roles/", json={"name": "DeleteTestRole"})
    role_id = create_response.json()["id"]
    
    # Delete the role
    response = client.delete(f"/roles/{role_id}")
    assert response.status_code == 204
    
    # Verify role is deleted
    get_response = client.get(f"/roles/{role_id}")
    assert get_response.status_code == 404


def test_delete_superuser_role():
    """Test that Superuser role cannot be deleted"""
    # Assuming Superuser role has ID 1
    response = client.delete("/roles/1")
    assert response.status_code == 403
    assert "Cannot delete Superuser role" in response.json()["detail"]
