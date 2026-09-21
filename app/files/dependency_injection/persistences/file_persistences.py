from dependency_injector import containers, providers

from app.files.persistences.postgres.file_postgres_persistence_service import (
    FilePostgresPersistenceService,
)


class FilePersistences(containers.DeclarativeContainer):
    """Container for file persistence implementations."""

    postgres = providers.Singleton(FilePostgresPersistenceService)

    carlemany = postgres
