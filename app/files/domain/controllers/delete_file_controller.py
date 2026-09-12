from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class DeleteFileController:
    """Controller for deleting a file."""

    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, file_id: int, user_id: int) -> None:
        """Delete a file."""
        await self.file_persistence.delete_file(file_id, user_id)
