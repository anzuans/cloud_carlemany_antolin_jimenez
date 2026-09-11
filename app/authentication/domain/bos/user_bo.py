from typing import Optional

from pydantic import BaseModel


class UserBO(BaseModel):
    id: Optional[int] = None
    email: str
    hashed_password: str
    address: Optional[str] = None
