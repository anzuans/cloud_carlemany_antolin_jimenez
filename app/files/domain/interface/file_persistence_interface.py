from abc import ABC, abstractmethod

from app.files.domain.bos.file_bo import FileBO


class FilePersistenceInterface(ABC):
    """Interface for file persistence operations."""

    @abstractmethod
    async def store_file(self, file_bo: FileBO) -> FileBO:
        """Store a file in the database."""
        pass

    @abstractmethod
    async def get_file(self, file_id: int, user_id: int) -> FileBO:
        """Get a file by ID, verifying ownership."""
        pass

    @abstractmethod
    async def get_files_by_user(self, user_id: int) -> list[FileBO]:
        """Get all files owned by a user."""
        pass

    @abstractmethod
    async def update_file_content(self, file_id: int, user_id: int, content: str) -> FileBO:
        """Update file content, verifying ownership."""
        pass

    @abstractmethod
    async def delete_file(self, file_id: int, user_id: int) -> None:
        """Delete a file, verifying ownership."""
        pass
