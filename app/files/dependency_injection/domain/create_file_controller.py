from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.create_file_controller import CreateFileController


class CreateFileControllers(containers.DeclarativeContainer):
    """Container for CreateFileController."""

    v1 = providers.Singleton(
        CreateFileController,
        file_persistence=FilePersistences.carlemany(),
    )

    carlemany = v1
