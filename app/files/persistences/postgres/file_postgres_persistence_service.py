from app.files.domain.bos.file_bo import FileBO
from app.files.domain.exceptions.FileNotFoundException import FileNotFoundException
from app.files.domain.exceptions.UnauthorizedFileAccessException import (
    UnauthorizedFileAccessException,
)
from app.files.domain.interface.file_persistence_interface import FilePersistenceInterface
from app.files.models import FileDB


class FilePostgresPersistenceService(FilePersistenceInterface):
    """PostgreSQL persistence implementation for files."""

    async def store_file(self, file_bo: FileBO) -> FileBO:
        """Store a file in the database."""
        file_db = await FileDB.create(
            title=file_bo.title,
            description=file_bo.description or "",
            content=file_bo.content or "",
            user_id=file_bo.user_id,
        )
        return FileBO(
            id=file_db.id,
            title=file_db.title,
            description=file_db.description,
            content=file_db.content,
            user_id=file_db.user_id,
        )

    async def get_file(self, file_id: int, user_id: int) -> FileBO:
        """Get a file by ID, verifying ownership."""
        file_db = await FileDB.get_or_none(id=file_id)
        if file_db is None:
            raise FileNotFoundException(f"File {file_id} not found")
        if file_db.user_id != user_id:
            raise UnauthorizedFileAccessException(
                f"User {user_id} does not own file {file_id}"
            )
        return FileBO(
            id=file_db.id,
            title=file_db.title,
            description=file_db.description,
            content=file_db.content,
            user_id=file_db.user_id,
        )

    async def get_files_by_user(self, user_id: int) -> list[FileBO]:
        """Get all files owned by a user."""
        files_db = await FileDB.filter(user_id=user_id)
        return [
            FileBO(
                id=file_db.id,
                title=file_db.title,
                description=file_db.description,
                content=file_db.content,
                user_id=file_db.user_id,
            )
            for file_db in files_db
        ]

    async def update_file_content(self, file_id: int, user_id: int, content: str) -> FileBO:
        """Update file content, verifying ownership."""
        file_db = await FileDB.get_or_none(id=file_id)
        if file_db is None:
            raise FileNotFoundException(f"File {file_id} not found")
        if file_db.user_id != user_id:
            raise UnauthorizedFileAccessException(
                f"User {user_id} does not own file {file_id}"
            )
        file_db.content = content
        await file_db.save()
        return FileBO(
            id=file_db.id,
            title=file_db.title,
            description=file_db.description,
            content=file_db.content,
            user_id=file_db.user_id,
        )

    async def delete_file(self, file_id: int, user_id: int) -> None:
        """Delete a file, verifying ownership."""
        file_db = await FileDB.get_or_none(id=file_id)
        if file_db is None:
            raise FileNotFoundException(f"File {file_id} not found")
        if file_db.user_id != user_id:
            raise UnauthorizedFileAccessException(
                f"User {user_id} does not own file {file_id}"
            )
        await file_db.delete()
