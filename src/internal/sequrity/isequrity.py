from abc import ABC, abstractmethod


class ISecurityService(ABC):
    @abstractmethod
    def hash_string(self, plain: str) -> str: ...

    @abstractmethod
    def generate_random_string(self, length: int=30) -> str: ...
    