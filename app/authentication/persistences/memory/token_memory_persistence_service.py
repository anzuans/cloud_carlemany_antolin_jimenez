from abc import ABC
from typing import Optional

from app.authentication.domain.interface.token_persistence_interface import (
    TokenPersistenceInterface,
)

from app.authentication.domain.exceptions.token_does_not_exists_exception import TokenDoesNotExistsException


class TokenMemoryPersistenceService(TokenPersistenceInterface, ABC):
    def __init__(self):
        self.token_db: dict[str, str] = {}

    def store_token(self, token: str, email: str) -> None:
        self.token_db[token] = email

    def get_email(self, token: str):
        if token not in self.token_persistence:
            raise TokenDoesNotExistsException
        return self.token_persistence[token]

    def delete_token(self, token: str) -> bool:
        if token not in self.token_db:
            return False

        del self.token_db[token]
        return True
