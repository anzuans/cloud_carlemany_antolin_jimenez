from dependency_injector import containers, providers

from app.authentication.persistences.memory.user_bo_memory_persistence_service import (
    UserBoMemoryPersistenceService,
)


class UserBOPersistences(containers.DeclarativeContainer):

    memory = providers.Singleton(
        UserBoMemoryPersistenceService,
    )

    carlemany = memory
