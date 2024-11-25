from backend.monitoring.monitor_service import MonitoringService
from ...models.database_models import SystemMetrics
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ...database.session import get_db
from ...auth.dependencies import get_current_active_user
from ...models.user_model import User
from ...services.network_monitor import NetworkMonitorService
from ...core.alert_system import AlertSystem

router = APIRouter()

@router.get("/health")
async def get_system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.check_system_health()

@router.get("/metrics")
async def get_system_metrics(db: Session = Depends(get_db)):
    monitoring_service = MonitoringService(db)
    return await monitoring_service.collect_metrics()

@router.get("/start")
async def start_monitoring(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Start network monitoring"""
    monitor = NetworkMonitorService(db)
    monitor.start_monitoring()
    return {"status": "success", "message": "Monitoring started"}

@router.get("/stop")
async def stop_monitoring(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Stop network monitoring"""
    monitor = NetworkMonitorService(db)
    monitor.stop_monitoring()
    return {"status": "success", "message": "Monitoring stopped"}

@router.get("/metrics")
async def get_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current metrics"""
    metrics = db.query(SystemMetrics).order_by(
        SystemMetrics.timestamp.desc()
    ).first()
    return metrics

@router.get("/alerts")
async def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get active alerts"""
    alert_system = AlertSystem(db)
    return alert_system.get_active_alerts() 