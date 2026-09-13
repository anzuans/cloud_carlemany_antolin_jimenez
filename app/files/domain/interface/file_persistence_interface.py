from abc import ABC, abstractmethod

from app.files.domain.bos.file_bo import FileBO


class FilePersistenceInterface(ABC):
    """Interface for file metadata persistence operations."""

    @abstractmethod
    async def store_file(self, file_bo: FileBO) -> FileBO:
        """Store file metadata in the database."""
        pass

    @abstractmethod
    async def get_file(self, file_id: int, user_id: int) -> FileBO:
        """Get file metadata by ID, verifying ownership."""
        pass

    @abstractmethod
    async def get_files_by_user(self, user_id: int) -> list[FileBO]:
        """Get all file metadata records owned by a user."""
        pass

    @abstractmethod
    async def update_file_content_info(
        self,
        file_id: int,
        user_id: int,
        content_path: str,
        original_filename: str,
    ) -> FileBO:
        """Update metadata that points to file content stored on disk."""
        pass

    @abstractmethod
    async def delete_file(self, file_id: int, user_id: int) -> None:
        """Delete file metadata, verifying ownership."""
        pass
