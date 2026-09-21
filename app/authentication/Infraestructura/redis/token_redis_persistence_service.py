import uuid

from app.authentication.domain.interface.token_persistence_interface import TokenPersistenceInterface

from redis import Redis
from app.authentication.domain.exceptions.token_does_not_exists_exception import TokenDoesNotExistsException
from app.config import redis_config

class TokenRedisPersistenceService(TokenPersistenceInterface):

    def __init__(self):
        self._redis = redis.Redis(
            host=redis_config.host,
            port=redis_config.port,
            db=redis_config.db,
            password=redis_config.password,
            decode_responses=True,
        )

    async def store_token(self, token: str, email: str, ttl: Optional[int] = 3600) -> None:
        """Almacena un token asociándolo al email del usuario con un TTL opcional."""
        if ttl:
            await self._redis.setex(name=token, time=ttl, value=email)
        else:
            await self._redis.set(name=token, value=email)

    async def get_email(self, token: str) -> Optional[str]:
        """Recupera el email del usuario asociado al token especificado."""
        return await self._redis.get(token)

    async def delete_token(self, token: str) -> bool:
        """Elimina el token de la base de datos de Redis."""
        deleted_count = await self._redis.delete(token)
        return deleted_count > 0