from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.exceptions.EmailDoesNotExistsException import (
    EmailDoesNotExistsException,
)
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

    async def __call__(self, token: str) -> UserBO:
        email = self.token_persistence_service.get_email(token)
        if email is None:
            raise InvalidTokenException()

        try:
            return await self.user_persistence_service.get_user(email)
        except EmailDoesNotExistsException:
            raise InvalidTokenException() from None
