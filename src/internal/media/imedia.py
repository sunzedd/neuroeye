from abc import ABC, abstractmethod
from typing import Any, Dict

class IMediaService(ABC):
    @staticmethod
    def create(url: str) -> Dict: ...

    @staticmethod
    @abstractmethod
    def create_from_file(image: Any) -> Dict: ...

    @staticmethod
    @abstractmethod
    def find_image(id: int) -> Dict: ...

    @staticmethod
    @abstractmethod
    def delete_image(id: int): ...

    @staticmethod
    @abstractmethod
    def get_url(id: int): ...
