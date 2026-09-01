"""Routes for authentication actions."""

import uuid
from hashlib import sha256
from typing import Optional

from fastapi import APIRouter, Body, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/authentication", tags=["authentication"])

user_database = {}
token_database = {}


class UserBo(BaseModel):
    email: str
    hashed_password: str
    address: Optional[str] = None


class RegisterInput(BaseModel):
    """Input for user registration."""

    email: str
    password: str
    address: Optional[str] = None


def generate_hashed_password(email: str, password: str) -> str:
    return sha256((email + password).encode()).digest().hex()


@router.post("/register")
async def register(input: RegisterInput = Body()) -> dict[str, str]:
    """Register a new user."""
    if input.email in user_database:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = generate_hashed_password(input.email, input.password)
    user_bo = UserBo(email=input.email, hashed_password=hashed_password, address=input.address)
    user_database[user_bo.email] = user_bo

    return {"status": "ok"}


class LoginInput(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(input: LoginInput = Body()) -> dict[str, str]:
    """Log a user in."""
    if input.email not in user_database:
        raise HTTPException(status_code=403, detail="Forbidden")

    hashed_password = generate_hashed_password(input.email, input.password)

    user_bo = user_database[input.email]

    if user_bo.password != hashed_password:
        raise HTTPException(status_code=403, detail="Forbidden")

    current_token = str(uuid.uuid4())
    token_database[current_token] = input.email

    return {"token": current_token}


@router.post("/logout")
async def logout(auth: str = Header()) -> dict[str, str]:
    """Log the current user out."""
    if auth not in token_database:
        raise HTTPException(status_code=403, detail="Forbidden")

    del token_database[auth]

    return {"detail": "Logout endpoint"}


class RegisterOutput(BaseModel):
    email: str
    address: Optional[str] = None


@router.get("/introspect")
async def introspect(auth: str = Header()) -> RegisterOutput:
    """Return information about the current authentication state."""
    if auth not in token_database:
        raise HTTPException(status_code=403, detail="Forbidden")

    current_email = token_database[auth]
    current_user = user_database[current_email]

    return RegisterOutput(email=current_email, address=current_user.address)
