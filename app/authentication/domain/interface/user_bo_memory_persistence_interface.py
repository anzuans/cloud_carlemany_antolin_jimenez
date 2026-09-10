from abc import ABC, abstractmethod
from typing import Optional

from app.authentication.domain.bos.user_bo import UserBO


class UserBOPersistenceInterface(ABC):

    @abstractmethod
    def exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def store_user(self, user_bo: UserBO):
        pass

    @abstractmethod
    def get_user(self, email: str) -> Optional[UserBO]:
        pass
