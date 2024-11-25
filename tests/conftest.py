import pytest
import sys
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from backend.models.database_models import Base

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test database URL
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://ids_user:123@localhost:5432/ids_test_db"
)

@pytest.fixture(scope="session")
def engine():
    """Create test database and return engine"""
    test_engine = create_engine(TEST_DATABASE_URL)
    if not database_exists(test_engine.url):
        create_database(test_engine.url)
    
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    yield test_engine
    
    # Drop test database after tests
    if database_exists(test_engine.url):
        test_engine.dispose()

@pytest.fixture(scope="session")
def TestingSessionLocal(engine):
    """Create session factory"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

@pytest.fixture(scope="function")
def db(TestingSessionLocal):
    """Get DB session"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="session")
def test_app(engine):
    """Create test application"""
    from backend.main import app
    from backend.database.session import get_db
    
    # Override the DB dependency
    async def override_get_db():
        session = TestingSessionLocal(bind=engine)
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    return app

@pytest.fixture(scope="session")
def test_client(test_app):
    """Create test client"""
    from fastapi.testclient import TestClient
    return TestClient(test_app)

# Configure asyncio
@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 