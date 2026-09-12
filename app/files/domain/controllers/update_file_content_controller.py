from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class UpdateFileContentController:
    """Controller for updating file content."""

    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, file_id: int, user_id: int, content: str) -> None:
        """Update file content."""
        await self.file_persistence.update_file_content(file_id, user_id, content)
