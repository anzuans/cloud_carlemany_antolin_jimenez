from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.list_files_controller import ListFilesController


class ListFilesControllers(containers.DeclarativeContainer):
    """Container for ListFilesController."""

    v1 = providers.Singleton(
        ListFilesController,
        file_persistence=FilePersistences.carlemany(),
    )

    carlemany = v1
