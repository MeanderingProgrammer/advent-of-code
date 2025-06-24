from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    @abstractmethod
    def info(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
