from dependency_injector import containers, providers

from app.authentication.persistences.memory.token_memory_persistence_service import (
    TokenMemoryPersistenceService,
)


class TokenPersistences(containers.DeclarativeContainer):
    memory = providers.Singleton(TokenMemoryPersistenceService)

    redis = providers.Singleton(TokenRedisPersistenceService)

    carlemany = redis
