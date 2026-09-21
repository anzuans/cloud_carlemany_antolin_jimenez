from abc import ABC, abstractmethod

from app.files.domain.bos.file_bo import FileBO


class FileContentPersistenceInterface(ABC):
    """Interface for file content persistence operations on disk."""

    @abstractmethod
    async def save_file_content(
        self,
        file_bo: FileBO,
        content: bytes,
        original_filename: str,
    ) -> str:
        """Store file content on disk and return the relative path."""
        pass

    @abstractmethod
    async def delete_file_content(self, file_bo: FileBO) -> None:
        """Delete file content from disk if it exists."""
        pass

    @abstractmethod
    async def merge_pdf_contents(
        self,
        source_paths: list[str],
        target_file_bo: FileBO,
        original_filename: str,
    ) -> str:
        """Merge multiple PDF files into a new file on disk and return its path."""
        pass