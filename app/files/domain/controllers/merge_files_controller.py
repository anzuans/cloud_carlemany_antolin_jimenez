from app.files.domain.bos.file_bo import FileBO
from app.files.domain.exceptions.FileNotFoundException import FileNotFoundException
from app.files.domain.interface.file_content_persistence_interface import (
    FileContentPersistenceInterface,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class MergeFilesController:
    """Controller for merging PDF files."""

    def __init__(
        self,
        file_persistence: FilePersistenceInterface,
        file_content_persistence: FileContentPersistenceInterface,
    ):
        self.file_persistence = file_persistence
        self.file_content_persistence = file_content_persistence

    async def __call__(self, file_ids: list[int], user_id: int) -> int:
        """Merge multiple PDF files."""
        files: list[FileBO] = []
        source_paths: list[str] = []
        for file_id in file_ids:
            file_bo = await self.file_persistence.get_file(file_id, user_id)
            if not file_bo.content_path:
                raise FileNotFoundException(f"File {file_id} has no content")
            files.append(file_bo)
        merged_title = "_".join([f.title for f in files]) + "_merged"
        merged_file = await self.file_persistence.store_file(
            FileBO(
                title=merged_title,
                description=f"Merged file from {len(files)} files",
                user_id=user_id,
            )
        )
        for file_bo in files:
            source_paths.append(file_bo.content_path)

        merged_content_path = await self.file_content_persistence.merge_pdf_contents(
            source_paths=source_paths,
            target_file_bo=merged_file,
            original_filename=f"{merged_title}.pdf",
        )
        try:
            await self.file_persistence.update_file_content_info(
                file_id=merged_file.id,
                user_id=user_id,
                content_path=merged_content_path,
                original_filename=f"{merged_title}.pdf",
            )
            return merged_file.id
        except Exception:
            await self.file_persistence.delete_file(merged_file.id, user_id)
            await self.file_content_persistence.delete_file_content(
                FileBO(
                    id=merged_file.id,
                    title=merged_file.title,
                    description=merged_file.description,
                    content_path=merged_content_path,
                    original_filename=f"{merged_title}.pdf",
                    user_id=user_id,
                )
            )
            raise
