import abc
from dataclasses import dataclass, field
from pathlib import Path

from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Language(abc.ABC):
    _setup: bool = field(default=False, repr=False)
    name: str
    solution_file: str

    def solution_path(self, day: Day) -> Path:
        return day.dir().joinpath(self.solution_file)

    def setup_commands(self) -> list[list[str]]:
        if self._setup:
            return []
        self._setup = True
        return self._setup_commands()

    @abc.abstractmethod
    def _setup_commands(self) -> list[list[str]]:
        pass

    @abc.abstractmethod
    def run_command(self, day: Day, run_args: list[str]) -> list[str]:
        pass

    @abc.abstractmethod
    def template_processing(self, day: Day) -> None:
        pass
