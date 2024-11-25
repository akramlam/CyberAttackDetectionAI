import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Test database URL
TEST_DATABASE_URL = "postgresql://ids_user:123@localhost:5432/ids_test_db"

# Create test database engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally: 
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health_endpoint_unauthorized():
    """Test health endpoint without authentication"""
    response = client.get("/api/monitoring/health")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_auth_flow():
    """Test authentication flow"""
    # Test registration
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 200
    assert "id" in response.json()

    # Test login
    login_data = {
        "username": "testuser",
        "password": "testpassword123",
        "grant_type": "password"
    }
    response = client.post("/api/auth/token", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    return token_data["access_token"]

def test_protected_endpoints():
    """Test protected endpoints with authentication"""
    token = test_auth_flow()
    headers = {"Authorization": f"Bearer {token}"}

    # Test health endpoint
    response = client.get("/api/monitoring/health", headers=headers)
    assert response.status_code == 200
    assert "status" in response.json()

    # Test metrics endpoint
    response = client.get("/api/monitoring/metrics", headers=headers)
    assert response.status_code == 200
    assert "cpu_usage" in response.json()

    # Test anomalies endpoint
    response = client.get("/api/anomalies", headers=headers)
    assert response.status_code == 200
    assert "anomalies" in response.json()

def test_traffic_monitoring():
    """Test traffic monitoring functionality"""
    token = test_auth_flow()
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/traffic/current", headers=headers)
    assert response.status_code == 200
    traffic_data = response.json()
    assert "total_packets" in traffic_data 