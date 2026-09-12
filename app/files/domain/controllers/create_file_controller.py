from app.files.domain.bos.file_bo import FileBO
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class CreateFileController:
    """Controller for creating a new file."""

    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, title: str, description: str, user_id: int) -> FileBO:
        """Create a new file."""
        file_bo = FileBO(
            title=title,
            description=description,
            content="",
            user_id=user_id,
        )
        return await self.file_persistence.store_file(file_bo)
