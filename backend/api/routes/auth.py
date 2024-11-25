from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...database.session import get_db
from ...models.user_model import User
from ...schemas.user import UserCreate, UserResponse, Token
from ...security.security_service import SecurityService
from typing import Annotated

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    security_service = SecurityService(db, "your-secret-key")
    hashed_password = User.get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """Login to get access token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not User.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    security_service = SecurityService(db, "your-secret-key")
    access_token = security_service.generate_token({"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"} 