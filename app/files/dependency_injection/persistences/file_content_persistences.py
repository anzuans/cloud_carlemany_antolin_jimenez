from dependency_injector import containers, providers

from app.files.persistences.local.file_content_local_persistence_service import (
    FileContentLocalPersistenceService,
)


class FileContentPersistences(containers.DeclarativeContainer):
    """Container for file content persistence implementations."""

    local = providers.Singleton(FileContentLocalPersistenceService)

    carlemany = local