from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class NetworkEvent(Base):
    __tablename__ = 'network_events'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String)
    dest_ip = Column(String)
    protocol = Column(String)
    length = Column(Integer)
    alert_level = Column(Integer)
    features = Column(JSON)
    anomaly_score = Column(Float)

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_event(self, event_data: dict):
        event = NetworkEvent(**event_data)
        self.session.add(event)
        self.session.commit()
    
    def get_recent_events(self, limit: int = 100):
        return self.session.query(NetworkEvent)\
            .order_by(NetworkEvent.timestamp.desc())\
            .limit(limit)\
            .all() 