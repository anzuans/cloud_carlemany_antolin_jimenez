from app.files.domain.interface.file_content_persistence_interface import (
    FileContentPersistenceInterface,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class DeleteFileController:
    """Controller for deleting a file."""

    def __init__(
        self,
        file_persistence: FilePersistenceInterface,
        file_content_persistence: FileContentPersistenceInterface,
    ):
        self.file_persistence = file_persistence
        self.file_content_persistence = file_content_persistence

    async def __call__(self, file_id: int, user_id: int) -> None:
        """Delete a file."""
        file_bo = await self.file_persistence.get_file(file_id, user_id)
        await self.file_content_persistence.delete_file_content(file_bo)
        await self.file_persistence.delete_file(file_id, user_id)
