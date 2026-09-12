from app.files.domain.bos.file_bo import FileBO
from app.files.domain.exceptions.FileNotFoundException import FileNotFoundException
from app.files.domain.exceptions.UnauthorizedFileAccessException import (
    UnauthorizedFileAccessException,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class GetFileController:
    """Controller for retrieving a specific file."""

    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, file_id: int, user_id: int) -> FileBO:
        """Get a file by ID."""
        return await self.file_persistence.get_file(file_id, user_id)
