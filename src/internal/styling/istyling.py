from abc import ABC, abstractmethod
from typing import Dict, List


class IStylingService(ABC):
    @abstractmethod
    def stylize(src_img_filepath: str, sample_img_filepath: str) -> Dict: ...
