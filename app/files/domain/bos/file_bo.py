from typing import Optional

from pydantic import BaseModel


class FileBO(BaseModel):
    """Business Object for Files."""

    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    user_id: int
