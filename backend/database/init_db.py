from sqlalchemy_utils import database_exists, create_database
from .session import engine
from ..models.database_models import Base
import logging

logger = logging.getLogger(__name__)

def init_database():
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info("Database created successfully")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise 