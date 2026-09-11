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
from app.authentication.models import UserDB


class UserBoPostgresPersistenceService(UserBOPersistenceInterface, ABC):
    def __init__(self):
        pass

    async def exists(self, email: str) -> bool:
        return await UserDB.filter(email=email).exists()

    async def store_user(self, user_bo: UserBO) -> None:
        if await self.exists(user_bo.email):
            raise EmailAlreadyExistsException()

        new_user = await UserDB.create(
            email=user_bo.email,
            password=user_bo.hashed_password,
            address=user_bo.address,
        )
        user_bo.id = new_user.id

    async def get_user(self, email: str) -> UserBO:
        user_db = await UserDB.get_or_none(email=email)
        if not user_db:
            raise EmailDoesNotExistsException()

        return UserBO(
            id=user_db.id,
            email=user_db.email,
            hashed_password=user_db.password,
            address=user_db.address,
        )
