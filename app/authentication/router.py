"""Routes for authentication actions."""

from fastapi import APIRouter

router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.post("/register")
async def register() -> dict[str, str]:
    """Register a new user."""
    return {"detail": "Registration endpoint"}


@router.post("/login")
async def login() -> dict[str, str]:
    """Log a user in."""
    return {"detail": "Login endpoint"}


@router.post("/logout")
async def logout() -> dict[str, str]:
    """Log the current user out."""
    return {"detail": "Logout endpoint"}


@router.get("/introspect")
async def introspect() -> dict[str, str]:
    """Return information about the current authentication state."""
    return {"detail": "Introspection endpoint"}
