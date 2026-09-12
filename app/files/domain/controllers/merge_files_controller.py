from pypdf import PdfMerger

from app.files.domain.bos.file_bo import FileBO
from app.files.domain.exceptions.FileNotFoundException import FileNotFoundException
from app.files.domain.exceptions.UnauthorizedFileAccessException import (
    UnauthorizedFileAccessException,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface


class MergeFilesController:
    """Controller for merging PDF files."""

    def __init__(self, file_persistence: FilePersistenceInterface):
        self.file_persistence = file_persistence

    async def __call__(self, file_ids: list[int], user_id: int) -> int:
        """Merge multiple PDF files."""
        files = []
        for file_id in file_ids:
            file_bo = await self.file_persistence.get_file(file_id, user_id)
            if not file_bo.content:
                raise FileNotFoundException(f"File {file_id} has no content")
            files.append(file_bo)

        merger = PdfMerger()
        for file_bo in files:
            if file_bo.content:
                merger.append(file_bo.content)

        merged_title = "_".join([f.title for f in files]) + "_merged"
        merged_content_filename = f"files/{merged_title}.pdf"

        merger.write(merged_content_filename)
        merger.close()

        # Create new file with merged content
        merged_file = FileBO(
            title=merged_title,
            description=f"Merged file from {len(files)} files",
            content=merged_content_filename,
            user_id=user_id,
        )
        result = await self.file_persistence.store_file(merged_file)
        return result.id
