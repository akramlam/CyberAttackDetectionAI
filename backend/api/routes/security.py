from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ...security.security_service import SecurityService
from ...database.session import get_db
from ...auth.dependencies import get_current_active_user
from ...models.user_model import User
from typing import Dict

router = APIRouter()

@router.post("/events")
async def log_security_event(
    event_data: Dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Log a security event"""
    security_service = SecurityService(db, "your-secret-key")
    try:
        security_service.log_security_event(event_data)
        return {"status": "success", "message": "Event logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events")
async def get_security_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get security events"""
    security_service = SecurityService(db, "your-secret-key")
    try:
        events = security_service.get_security_events()
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 