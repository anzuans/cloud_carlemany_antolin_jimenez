from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.get_file_controller import GetFileController


class GetFileControllers(containers.DeclarativeContainer):
    """Container for GetFileController."""

    v1 = providers.Singleton(
        GetFileController,
        file_persistence=FilePersistences.carlemany(),
    )

    carlemany = v1
