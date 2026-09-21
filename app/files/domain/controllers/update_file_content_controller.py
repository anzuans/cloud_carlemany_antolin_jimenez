from fastapi import UploadFile

from app.files.domain.bos.file_bo import FileBO
from app.files.domain.interface.file_content_persistence_interface import (
    FileContentPersistenceInterface,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class UpdateFileContentController:
    """Controller for updating file content."""

    def __init__(
        self,
        file_persistence: FilePersistenceInterface,
        file_content_persistence: FileContentPersistenceInterface,
    ):
        self.file_persistence = file_persistence
        self.file_content_persistence = file_content_persistence

    async def __call__(self, file_id: int, user_id: int, upload_file: UploadFile) -> FileBO:
        """Update file content stored on disk."""
        file_bo = await self.file_persistence.get_file(file_id, user_id)
        content = await upload_file.read()
        original_filename = upload_file.filename or "uploaded_file"
        content_path = await self.file_content_persistence.save_file_content(
            file_bo=file_bo,
            content=content,
            original_filename=original_filename,
        )

        try:
            return await self.file_persistence.update_file_content_info(
                file_id=file_id,
                user_id=user_id,
                content_path=content_path,
                original_filename=original_filename,
            )
        except Exception:
            await self.file_content_persistence.delete_file_content(
                FileBO(
                    id=file_id,
                    title=file_bo.title,
                    description=file_bo.description,
                    content_path=content_path,
                    original_filename=original_filename,
                    user_id=user_id,
                )
            )
            raise
