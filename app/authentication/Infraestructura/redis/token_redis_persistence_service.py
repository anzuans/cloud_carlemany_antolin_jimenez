import uuid

from app.authentication.domain.interface.token_persistence_interface import TokenPersistenceInterface

from redis import Redis
from app.authentication.domain.exceptions.token_does_not_exists_exception import TokenDoesNotExistsException
from app.config import redis_config

class TokenRedisPersistenceInterface(TokenPersistenceInterface):

    def __init__(self):
        self._redis_client = Redis(
            host=redis_config.host,
            port=redis_config.port,
            decode_responses=True
        )

    def generate_token(self, email: str) -> str:
        current_token = str(uuid.uuid4())
        self._redis_client.set(current_token, email)
        return current_token

    def get_email(self, token: str) -> str:
        if not self._redis_client.exists(token):
            raise TokenDoesNotExistsException()
        return self._redis_client.get(token)

    def delete_token(self, token: str):
        self._redis_client.delete(token)