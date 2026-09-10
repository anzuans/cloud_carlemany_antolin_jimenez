"""Routes for authentication actions."""

from typing import Optional

from fastapi import APIRouter, Body, Header, HTTPException
from pydantic import BaseModel

from app.authentication.dependency_injection.domain.introspect_controller import (
    IntrospectControllers,
)
from app.authentication.dependency_injection.domain.login_controller import LoginControllers
from app.authentication.dependency_injection.domain.logout_controller import LogoutControllers
from app.authentication.dependency_injection.domain.register_controller import RegisterControllers
from app.authentication.domain.exceptions.EmailAlreadyExistsException import (
    EmailAlreadyExistsException,
)
from app.authentication.domain.exceptions.InvalidCredentialsException import (
    InvalidCredentialsException,
)
from app.authentication.domain.exceptions.InvalidTokenException import InvalidTokenException

router = APIRouter(prefix="/authentication", tags=["authentication"])


class RegisterInput(BaseModel):
    """Input for user registration."""

    email: str
    password: str
    address: Optional[str] = None


@router.post("/register")
async def register(input: RegisterInput = Body()) -> dict[str, str]:
    """Register a new user."""
    register_controller = RegisterControllers.carlemany()

    try:
        register_controller(email=input.email, password=input.password, address=input.address)
    except EmailAlreadyExistsException:
        raise HTTPException(status_code=400, detail="Email already registered") from None

    return {"status": "ok"}


class LoginInput(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(input: LoginInput = Body()) -> dict[str, str]:
    """Log a user in."""
    login_controller = LoginControllers.carlemany()

    try:
        token = login_controller(email=input.email, password=input.password)
    except InvalidCredentialsException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return {"token": token}


@router.post("/logout")
async def logout(auth: str = Header()) -> dict[str, str]:
    """Log the current user out."""
    logout_controller = LogoutControllers.carlemany()

    try:
        logout_controller(token=auth)
    except InvalidTokenException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return {"detail": "Logout endpoint"}


class RegisterOutput(BaseModel):
    email: str
    address: Optional[str] = None


@router.get("/introspect")
async def introspect(auth: str = Header()) -> RegisterOutput:
    """Return information about the current authentication state."""
    introspect_controller = IntrospectControllers.carlemany()

    try:
        user_bo = introspect_controller(token=auth)
    except InvalidTokenException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return RegisterOutput(email=user_bo.email, address=user_bo.address)
