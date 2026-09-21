from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_content_persistences import (
    FileContentPersistences,
)
from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.update_file_content_controller import UpdateFileContentController


class UpdateFileContentControllers(containers.DeclarativeContainer):
    """Container for UpdateFileContentController."""

    v1 = providers.Singleton(
        UpdateFileContentController,
        file_persistence=FilePersistences.carlemany(),
        file_content_persistence=FileContentPersistences.carlemany(),
    )

    carlemany = v1
