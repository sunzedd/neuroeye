from abc import ABC, abstractmethod
from typing import Dict


class IAuthService(ABC):
    @staticmethod
    @abstractmethod
    def signin(username: str, password: str) -> Dict: ...

    @staticmethod
    @abstractmethod
    def signout(session_key: str): ...

    @staticmethod
    @abstractmethod
    def get_authenticated_user_id(session_key: str) -> int: ...

    @staticmethod
    @abstractmethod
    def create(user_id: int) -> Dict: ...


class AuthInvalidCredentialsError(Exception):
    pass
