from typing import Optional

from app.authentication.domain.bos.user_bo import UserBO
from app.authentication.domain.interface.user_bo_memory_persistence_interface import (
    UserBOPersistenceInterface,
)
from app.authentication.domain.services.generate_hash_service import GenerateHashService


class RegisterController:
    def __init__(self, persistence_service: UserBOPersistenceInterface):
        self.generate_hash_service = GenerateHashService()
        self.persistence_service = persistence_service

    def __call__(self, email: str, password: str, address: Optional[str] = None):
        hashed_password = self.generate_hash_service(email, password)
        user_bo = UserBO(email=email, hashed_password=hashed_password, address=address)
        self.persistence_service.store_user(user_bo)
