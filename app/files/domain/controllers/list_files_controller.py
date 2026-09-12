from app.files.domain.bos.file_bo import FileBO
from app.files.domain.exceptions.FileNotFoundException import FileNotFoundException
from app.files.domain.exceptions.UnauthorizedFileAccessException import (
    UnauthorizedFileAccessException,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class ListFilesController:
    """Controller for listing files owned by a user."""

    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, user_id: int) -> list[FileBO]:
        """List files for a user."""
        return await self.file_persistence.get_files_by_user(user_id)
