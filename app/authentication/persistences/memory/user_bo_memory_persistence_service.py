from abc import ABC
from typing import Optional

from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.exceptions.EmailAlreadyExistsException import (
    EmailAlreadyExistsException,
)
from app.authentication.domain.interface.user_bo_memory_persistence_interface import (
    UserBOPersistenceInterface,
)


class UserBoMemoryPersistenceService(UserBOPersistenceInterface, ABC):
    def __init__(self):
        self.user_db = {}

    def exists(self, email: str) -> bool:
        return email in self.user_db

    def store_user(self, user_bo: UserBO):
        if self.exists(user_bo.email):
            raise EmailAlreadyExistsException()

        self.user_db[user_bo.email] = user_bo

    def get_user(self, email: str) -> Optional[UserBO]:
        return self.user_db.get(email)
