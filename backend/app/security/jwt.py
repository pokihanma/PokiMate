from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import get_settings

settings = get_settings()
ALGORITHM = "HS256"


def create_access_token(sub: str, user_id: int, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.astra_jwt_access_minutes)
    payload = {"sub": sub, "user_id": user_id, "role": role, "type": "access", "exp": expire}
    return jwt.encode(payload, settings.astra_jwt_secret, algorithm=ALGORITHM)


def create_refresh_token(sub: str, user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.astra_jwt_refresh_days)
    payload = {"sub": sub, "user_id": user_id, "type": "refresh", "exp": expire}
    return jwt.encode(payload, settings.astra_jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.astra_jwt_secret, algorithms=[ALGORITHM])
    except JWTError:
        return None
