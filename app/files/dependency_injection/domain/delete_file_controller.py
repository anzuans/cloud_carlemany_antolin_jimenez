from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.delete_file_controller import DeleteFileController


class DeleteFileControllers(containers.DeclarativeContainer):
    """Container for DeleteFileController."""

    v1 = providers.Singleton(
        DeleteFileController,
        file_persistence=FilePersistences.carlemany(),
    )

    carlemany = v1
