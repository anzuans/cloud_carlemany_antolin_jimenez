from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.exceptions.InvalidTokenException import InvalidTokenException
from app.authentication.domain.interface.token_persistence_interface import (
    TokenPersistenceInterface,
)
from app.authentication.domain.interface.user_bo_memory_persistence_interface import (
    UserBOPersistenceInterface,
)


class IntrospectController:
    def __init__(
        self,
        user_persistence_service: UserBOPersistenceInterface,
        token_persistence_service: TokenPersistenceInterface,
    ):
        self.user_persistence_service = user_persistence_service
        self.token_persistence_service = token_persistence_service

    def __call__(self, token: str) -> UserBO:
        email = self.token_persistence_service.get_email(token)
        user_bo = self.user_persistence_service.get_user(email) if email else None

        if user_bo is None:
            raise InvalidTokenException()

        return user_bo
