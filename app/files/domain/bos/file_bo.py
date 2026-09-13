from typing import Optional

from pydantic import BaseModel


class FileBO(BaseModel):
    """Business Object for Files."""

    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    content_path: Optional[str] = None
    original_filename: Optional[str] = None
    user_id: int
