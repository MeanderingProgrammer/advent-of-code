import abc
import subprocess
import time
from dataclasses import dataclass, field
from typing import List

from pojo.day import Day


@dataclass(kw_only=True, init=False)
class Language(abc.ABC):
    _setup: bool = field(default=False, repr=False)
    name: str
    solution_file: str

    def setup(self) -> None:
        if not self._setup:
            command = self._setup_command()
            self._execute(command)
        self._setup = True

    @abc.abstractmethod
    def _setup_command(self) -> List[str]:
        pass

    def run(self, day: Day, run_args: List[str]) -> float:
        command = self._run_command(day, run_args)
        start = time.time()
        self._execute(command)
        return time.time() - start

    @abc.abstractmethod
    def _run_command(self, day: Day, run_args: List[str]) -> List[str]:
        pass

    def _execute(self, command: List[str]) -> None:
        if len(command) == 0:
            return
        result = subprocess.run(command, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"Failed due to: {result.stderr.decode()}")

    @abc.abstractmethod
    def template_processing(self, day: Day) -> None:
        pass
