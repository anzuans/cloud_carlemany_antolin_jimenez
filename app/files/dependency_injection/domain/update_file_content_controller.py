from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.update_file_content_controller import UpdateFileContentController


class UpdateFileContentControllers(containers.DeclarativeContainer):
    """Container for UpdateFileContentController."""

    v1 = providers.Singleton(
        UpdateFileContentController,
        file_persistence=FilePersistences.carlemany(),
    )

    carlemany = v1
