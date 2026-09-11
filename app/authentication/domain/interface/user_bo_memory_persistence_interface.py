from abc import ABC, abstractmethod

from app.authentication.domain.bos.user_bo import UserBO


class UserBOPersistenceInterface(ABC):

    @abstractmethod
    async def exists(self, email: str) -> bool:
        pass

    @abstractmethod
    async def store_user(self, user_bo: UserBO):
        pass

    @abstractmethod
    async def get_user(self, email: str) -> UserBO:
        pass
