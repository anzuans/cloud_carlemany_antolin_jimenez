from __future__ import annotations

import asyncio
from pathlib import Path
from uuid import uuid4

from pypdf import PdfMerger

from app.files.domain.bos.file_bo import FileBO
from app.files.domain.interface.file_content_persistence_interface import (
    FileContentPersistenceInterface,
)


class FileContentLocalPersistenceService(FileContentPersistenceInterface):
    """Local filesystem persistence implementation for file content."""

    def __init__(self) -> None:
        self.base_directory = Path("files/storage")
        self.base_directory.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        return Path(filename).name.replace(" ", "_")

    def _build_path(self, file_bo: FileBO, original_filename: str) -> Path:
        sanitized_filename = self._sanitize_filename(original_filename)
        return self.base_directory / f"{file_bo.id}_{uuid4().hex}_{sanitized_filename}"

    async def save_file_content(
        self,
        file_bo: FileBO,
        content: bytes,
        original_filename: str,
    ) -> str:
        """Store file content on disk and return the relative path."""
        content_path = self._build_path(file_bo, original_filename)
        await asyncio.to_thread(content_path.write_bytes, content)
        return str(content_path)

    async def delete_file_content(self, file_bo: FileBO) -> None:
        """Delete file content from disk if it exists."""
        if not file_bo.content_path:
            return
        content_path = Path(file_bo.content_path)
        if content_path.exists():
            await asyncio.to_thread(content_path.unlink)

    async def merge_pdf_contents(
        self,
        source_paths: list[str],
        target_file_bo: FileBO,
        original_filename: str,
    ) -> str:
        """Merge multiple PDF files into a new file on disk and return its path."""
        target_path = self._build_path(target_file_bo, original_filename)

        def _merge() -> None:
            merger = PdfMerger()
            try:
                for source_path in source_paths:
                    merger.append(source_path)
                merger.write(str(target_path))
            finally:
                merger.close()

        await asyncio.to_thread(_merge)
        return str(target_path)