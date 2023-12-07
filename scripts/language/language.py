import abc
from dataclasses import dataclass
from pathlib import Path

from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Language(abc.ABC):
    name: str
    solution_file: str

    def solution_path(self, day: Day) -> Path:
        return day.dir().joinpath(self.solution_file)

    @abc.abstractmethod
    def setup_commands(self) -> list[list[str]]:
        pass

    @abc.abstractmethod
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        pass

    @abc.abstractmethod
    def template_processing(self, day: Day) -> None:
        pass
