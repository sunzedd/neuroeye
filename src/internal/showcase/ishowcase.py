from abc import ABC, abstractmethod
from typing import Dict, List


class IShowcaseService(ABC):
    @staticmethod
    @abstractmethod
    def create(user_id: int, title: str, description: str, 
               src_img_id: int, sample_img_id: int, dst_img_id: int,
               publish: bool=False, tags: str=None) -> Dict:
        ...

    @staticmethod
    @abstractmethod
    def find(id: int) -> Dict: ...

    @staticmethod
    @abstractmethod
    def find_owned_by_user(user_id: int) -> List[Dict]: ...

    @staticmethod
    @abstractmethod
    def find_liked_by_user(user_id: int) -> List[Dict]: ...

    @staticmethod
    @abstractmethod
    def find_last_published(limit: int=30) -> List[Dict]: ...

    @staticmethod
    @abstractmethod
    def is_liked_by_user(showcase_id: int, user_id: int) -> bool: ...

    @staticmethod
    @abstractmethod
    def publish(id: int): ...

    @staticmethod
    @abstractmethod
    def unpublish(id: int): ...

    @staticmethod
    @abstractmethod
    def like(showcase_id: int, user_id: int): ...

    @staticmethod
    @abstractmethod
    def unlike(showcase_id: int, user_id: int): ...

    @staticmethod
    @abstractmethod
    def delete(id: int): ...

    @staticmethod
    @abstractmethod
    def increase_view_count(id: int): ...

    @staticmethod
    @abstractmethod
    def get_view_count(id: int) -> int: ...
