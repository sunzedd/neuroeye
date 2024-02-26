from abc import ABC, abstractmethod
from typing import Dict


class IUserService(ABC):
    @staticmethod
    @abstractmethod
    def create(username: str, email: str, password: str) -> Dict: ...

    @staticmethod
    @abstractmethod
    def find(id: int) -> Dict: ...

    @staticmethod
    @abstractmethod
    def find_by_username(username: str) -> Dict: ...

    @staticmethod
    @abstractmethod
    def update_password(id: int, new_password: str): ...

    @staticmethod
    @abstractmethod
    def update_userpic(id: int, new_userpic_id: int): ...

    @staticmethod
    @abstractmethod
    def validate_password(user_id: int, given_password: int) -> bool: ...


class UserDoesNotExistsError(Exception):
    pass
class UserAlreadyExistsError(Exception):
    pass
