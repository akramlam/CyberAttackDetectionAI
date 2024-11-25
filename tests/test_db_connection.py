from sqlalchemy import create_engine, inspect, text
from sqlalchemy_utils import database_exists
import pytest
from backend.models.database_models import Base

def test_database_connection(engine):
    """Test database connection"""
    assert database_exists(engine.url)

def test_table_creation(engine):
    """Test if all tables can be created"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables exist
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        assert "security_events" in existing_tables
        assert "system_metrics" in existing_tables
        assert "users" in existing_tables
        
        print("✅ Tables created successfully!")
    except Exception as e:
        pytest.fail(f"Table creation failed: {str(e)}")

def test_crud_operations(db):
    """Test basic CRUD operations"""
    from backend.models.database_models import SystemMetrics
    
    try:
        # Create test metric
        test_metric = SystemMetrics(
            cpu_usage=50.0,
            memory_usage=60.0,
            packet_count=100,
            anomaly_count=0
        )
        
        # Add and commit
        db.add(test_metric)
        db.commit()
        
        # Query back
        queried_metric = db.query(SystemMetrics).first()
        assert queried_metric is not None
        assert queried_metric.cpu_usage == 50.0
        
        print("✅ CRUD operations successful!")
    except Exception as e:
        pytest.fail(f"CRUD operations failed: {str(e)}") 