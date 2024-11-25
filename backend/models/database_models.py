from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class NetworkPacket(Base):
    __tablename__ = 'network_packets'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String)
    dest_ip = Column(String)
    protocol = Column(Integer)
    length = Column(Integer)
    payload = Column(String, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_score = Column(Float, nullable=True)

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_type = Column(String)
    severity = Column(String)
    message = Column(String)
    details = Column(JSON, nullable=True)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)

class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    packet_count = Column(Integer)
    anomaly_count = Column(Integer) 