import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app.models import User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def sample_user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "is_active": True
    }


def test_create_user(sample_user_data):
    """Test creating a new user"""
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["username"] == sample_user_data["username"]
    assert data["full_name"] == sample_user_data["full_name"]
    assert data["is_active"] == sample_user_data["is_active"]
    assert "id" in data
    assert "created_at" in data


def test_get_users():
    """Test getting all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_not_found():
    """Test getting a non-existent user"""
    response = client.get("/users/999")
    assert response.status_code == 404


def test_create_user_duplicate_email(sample_user_data):
    """Test creating a user with duplicate email"""
    # Create first user
    client.post("/users/", json=sample_user_data)
    
    # Try to create another user with same email
    duplicate_data = sample_user_data.copy()
    duplicate_data["username"] = "different_username"
    response = client.post("/users/", json=duplicate_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_create_user_duplicate_username(sample_user_data):
    """Test creating a user with duplicate username"""
    # Create first user
    client.post("/users/", json=sample_user_data)
    
    # Try to create another user with same username
    duplicate_data = sample_user_data.copy()
    duplicate_data["email"] = "different@example.com"
    response = client.post("/users/", json=duplicate_data)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]
