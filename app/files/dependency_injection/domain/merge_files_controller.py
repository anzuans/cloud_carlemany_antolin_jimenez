from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_persistences import FilePersistences
from app.files.domain.controllers.merge_files_controller import MergeFilesController


class MergeFilesControllers(containers.DeclarativeContainer):
    """Container for MergeFilesController."""

    v1 = providers.Singleton(
        MergeFilesController,
        file_persistence=FilePersistences.carlemany(),
    )

    carlemany = v1
