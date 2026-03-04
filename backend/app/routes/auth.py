from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    RefreshRequest,
)
from app.security.hashing import hash_password, verify_password
from app.security.jwt import create_access_token, create_refresh_token, decode_token
from app.security.deps import get_current_user
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
def register(body: RegisterRequest, session: Session = Depends(get_session)):
    settings = get_settings()
    count = session.exec(select(User)).all()
    is_first = len(count) == 0
    if not is_first:
        admin_only = getattr(settings, "astra_allow_register", False)
        if not admin_only:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Registration disabled")
    existing = session.exec(select(User).where(User.email == body.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    existing_u = session.exec(select(User).where(User.username == body.username)).first()
    if existing_u:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    role = "ADMIN" if is_first else "USER"
    user = User(
        email=body.email,
        username=body.username,
        password_hash=hash_password(body.password),
        role=role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"success": True, "data": {"id": user.id, "email": user.email, "username": user.username, "role": user.role}}


@router.post("/login", response_model=dict)
def login(body: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = create_access_token(str(user.id), user.id, user.role)
    refresh = create_refresh_token(str(user.id), user.id)
    expires_in = get_settings().astra_jwt_access_minutes * 60
    return {
        "success": True,
        "data": {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
            "expires_in": expires_in,
            "user": {"id": user.id, "email": user.email, "username": user.username, "role": user.role},
        },
    }


@router.post("/refresh", response_model=dict)
def refresh(body: RefreshRequest, session: Session = Depends(get_session)):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user_id = payload.get("user_id")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    access = create_access_token(str(user.id), user.id, user.role)
    expires_in = get_settings().astra_jwt_access_minutes * 60
    return {"success": True, "data": {"access_token": access, "token_type": "bearer", "expires_in": expires_in}}


@router.post("/logout")
def logout():
    return {"success": True, "data": None}


@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)):
    return {"success": True, "data": {"id": current_user.id, "email": current_user.email, "username": current_user.username, "role": current_user.role}}
