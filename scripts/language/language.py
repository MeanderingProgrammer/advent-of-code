import abc
import subprocess
import time
from typing import List

from pojo.day import Day


class Language(abc.ABC):
    def __init__(self):
        self.__setup = False

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def solution_file(self) -> str:
        pass

    def setup(self) -> None:
        if not self.__setup:
            command = self._setup_command()
            self._execute(command)
        self.__setup = True

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

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.name
