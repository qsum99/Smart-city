"""Local auth (PyJWT HS256, users in SQLite) — 09 §1 role matrix, LOCAL profile."""
from __future__ import annotations

import hashlib
import hmac
import os
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from services.common.config import settings
from services.common.db import session_scope
from services.common.tables import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

ROLES = ("citizen", "operator", "approver", "admin")
# role → allowed roles for require_role
ROLE_RANK = {"citizen": 0, "operator": 1, "approver": 2, "admin": 3}


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return f"{salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_hex, dk_hex = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 100_000)
        return hmac.compare_digest(dk.hex(), dk_hex)
    except Exception:
        return False


def ensure_users() -> None:
    """Seed demo users (idempotent)."""
    with session_scope() as s:
        for name, pwd, role, dept in (
            ("operator", "operator123", "operator", "OCC"),
            ("approver", "approver123", "approver", "OCC"),
            ("admin", "admin123", "admin", "IT"),
            ("citizen", "citizen123", "citizen", None),
        ):
            if s.scalar(select(User).where(User.username == name)) is None:
                s.add(User(username=name, password_hash=hash_password(pwd),
                           role=role, dept_id=dept))


def authenticate(username: str, password: str) -> User | None:
    with session_scope() as s:
        user = s.scalar(select(User).where(User.username == username))
        if user and verify_password(password, user.password_hash):
            return user
    return None


@dataclass
class TokenPayload:
    sub: str
    role: str
    dept_id: str | None


def issue_token(user: User) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": user.username,
        "role": user.role,
        "dept_id": user.dept_id,
        "iat": now,
        "exp": now + timedelta(seconds=settings.jwt_ttl_seconds),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> TokenPayload:
    data = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    return TokenPayload(sub=data["sub"], role=data["role"], dept_id=data.get("dept_id"))


def current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        return decode_token(token)
    except jwt.PyJWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc


def require_role(min_role: str):
    """Dependency factory: min role rank required (approver ⊇ operator ⊇ citizen)."""

    def _dep(user: TokenPayload = Depends(current_user)) -> TokenPayload:
        if ROLE_RANK.get(user.role, -1) < ROLE_RANK.get(min_role, 99):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"requires role {min_role}")
        return user

    return _dep
