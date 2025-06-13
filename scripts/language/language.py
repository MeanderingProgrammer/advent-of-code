from abc import ABC, abstractmethod
from pathlib import Path

from pojo.day import Day


class Language(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def file(self) -> str:
        pass

    @property
    @abstractmethod
    def cmd(self) -> str:
        pass

    def solution(self, day: Day) -> Path:
        return day.dir().joinpath(self.file)

    @abstractmethod
    def test_command(self) -> list[str]:
        pass

    @abstractmethod
    def build_commands(self) -> list[list[str]]:
        pass

    @abstractmethod
    def run_command(self, day: Day, args: list[str]) -> list[str]:
        pass

    @abstractmethod
    def add_build(self, day: Day) -> None:
        pass
