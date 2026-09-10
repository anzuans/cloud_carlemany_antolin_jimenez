import uuid

from app.authentication.domain.exceptions.InvalidCredentialsException import (
    InvalidCredentialsException,
)
from app.authentication.domain.interface.token_persistence_interface import (
    TokenPersistenceInterface,
)
from app.authentication.domain.interface.user_bo_memory_persistence_interface import (
    UserBOPersistenceInterface,
)
from app.authentication.domain.services.generate_hash_service import GenerateHashService


class LoginController:
    def __init__(
        self,
        user_persistence_service: UserBOPersistenceInterface,
        token_persistence_service: TokenPersistenceInterface,
    ):
        self.generate_hash_service = GenerateHashService()
        self.user_persistence_service = user_persistence_service
        self.token_persistence_service = token_persistence_service

    def __call__(self, email: str, password: str) -> str:
        user_bo = self.user_persistence_service.get_user(email)
        hashed_password = self.generate_hash_service(email, password)

        if user_bo is None or user_bo.hashed_password != hashed_password:
            raise InvalidCredentialsException()

        token = str(uuid.uuid4())
        self.token_persistence_service.store_token(token, email)
        return token
