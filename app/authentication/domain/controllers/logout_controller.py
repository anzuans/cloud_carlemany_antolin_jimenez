from app.authentication.domain.exceptions.InvalidTokenException import InvalidTokenException
from app.authentication.domain.interface.token_persistence_interface import (
    TokenPersistenceInterface,
)


class LogoutController:
    def __init__(self, token_persistence_service: TokenPersistenceInterface):
        self.token_persistence_service = token_persistence_service

    def __call__(self, token: str) -> None:
        if not self.token_persistence_service.delete_token(token):
            raise InvalidTokenException()
