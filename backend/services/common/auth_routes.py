"""Shared /auth/token route — mounted into every service (LOCAL profile)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from services.common.auth import authenticate, issue_token

router = APIRouter(tags=["auth"])


@router.post("/auth/token")
def token(form: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = authenticate(form.username, form.password)
    if user is None:
        raise HTTPException(401, detail="bad credentials")
    return {"access_token": issue_token(user), "token_type": "bearer", "role": user.role}
