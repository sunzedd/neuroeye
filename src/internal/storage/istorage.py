from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IDatabaseGateway(ABC):
    @abstractmethod
    def execute_query(self, sql: str, fetch_response: bool=True) -> List[tuple]: ...

class DatabaseSyncError(Exception):
    pass
