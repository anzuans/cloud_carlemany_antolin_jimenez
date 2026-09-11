from dependency_injector import containers, providers

from app.authentication.persistences.memory.user_bo_memory_persistence_service import (
    UserBoMemoryPersistenceService,
)
from app.authentication.persistences.postgres.user_bo_postgres_persistence_service import \
    UserBoPostgresPersistenceService


class UserBOPersistences(containers.DeclarativeContainer):

    memory = providers.Singleton(
        UserBoMemoryPersistenceService,
    )

    postgres = providers.Singleton(
        UserBoPostgresPersistenceService,
    )

    carlemany = postgres