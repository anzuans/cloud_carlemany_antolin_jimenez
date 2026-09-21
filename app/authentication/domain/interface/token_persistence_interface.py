from abc import ABC, abstractmethod
from typing import Optional


class TokenPersistenceInterface(ABC):
    @abstractmethod
    def store_token(self, token: str, email: str) -> None:
        pass

    @abstractmethod
    def generate_token(self, email: str) -> str:
        pass

    @abstractmethod
    def get_email(self, token: str) -> Optional[str]:
        pass

    @abstractmethod
    def delete_token(self, token: str) -> bool:
        pass
