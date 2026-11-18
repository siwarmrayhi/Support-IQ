"""Mots de passe et jetons d'authentification."""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from supportiq.config import settings

ALGORITHM = "HS256"
MAX_PASSWORD_BYTES = 72  # limite de bcrypt


def hash_password(password: str) -> str:
    data = password.encode("utf-8")
    if len(data) > MAX_PASSWORD_BYTES:
        raise ValueError("Mot de passe trop long (72 octets maximum)")
    return bcrypt.hashpw(data, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    data = password.encode("utf-8")
    if len(data) > MAX_PASSWORD_BYTES:
        return False
    return bcrypt.checkpw(data, password_hash.encode("utf-8"))


def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_minutes
    )
    payload = {"sub": str(user_id), "role": role, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None