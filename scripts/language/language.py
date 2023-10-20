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

    def initial_setup(self) -> None:
        if not self.__setup:
            self._run_setup()
        self.__setup = True

    @abc.abstractmethod
    def _run_setup(self) -> None:
        pass

    @abc.abstractmethod
    def compile(self) -> None:
        pass

    def run(self, day: Day, run_args: List[str]) -> float:
        start = time.time()
        command = self._get_run_command(day, run_args)
        result = subprocess.run(command, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"Failed due to: {result.stderr.decode()}")
        return time.time() - start

    @abc.abstractmethod
    def _get_run_command(self, day: Day, run_args: List[str]) -> List[str]:
        pass

    @abc.abstractmethod
    def template_processing(self, day: Day) -> None:
        pass

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.name
