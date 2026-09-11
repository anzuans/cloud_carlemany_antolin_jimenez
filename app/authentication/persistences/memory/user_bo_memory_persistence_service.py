from abc import ABC

from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.exceptions.EmailAlreadyExistsException import (
    EmailAlreadyExistsException,
)
from app.authentication.domain.exceptions.EmailDoesNotExistsException import (
    EmailDoesNotExistsException,
)
from app.authentication.domain.interface.user_bo_memory_persistence_interface import (
    UserBOPersistenceInterface,
)


class UserBoMemoryPersistenceService(UserBOPersistenceInterface, ABC):
    def __init__(self):
        self.user_db = {}

    async def exists(self, email: str) -> bool:
        return email in self.user_db

    async def store_user(self, user_bo: UserBO) -> None:
        if await self.exists(user_bo.email):
            raise EmailAlreadyExistsException()

        self.user_db[user_bo.email] = user_bo

    async def get_user(self, email: str) -> UserBO:
        user_bo = self.user_db.get(email)
        if user_bo is None:
            raise EmailDoesNotExistsException()

        return user_bo
