import abc
import time
import subprocess
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

    def initial_setup(self):
        if not self.__setup:
            self._run_setup()
        self.__setup = True

    @abc.abstractmethod
    def _run_setup(self):
        pass

    @abc.abstractmethod
    def compile(self, day: Day):
        pass

    def run(self, day: Day, run_args: List[str]) -> float:
        start = time.time()
        command = self._get_run_command(day, run_args)

        pipe = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)
        err = pipe.communicate()[1].decode()
        if len(err) > 0:
            raise Exception(f'Failed due to: {err}')

        return time.time() - start

    @abc.abstractmethod
    def _get_run_command(self, day: Day, run_args: List[str]) -> str:
        pass

    @abc.abstractmethod
    def template_processing(self, day: Day):
        pass


class InterprettedLanguage(Language):

    def compile(self, day: Day):
         # Interpreted languages do not need to be compiled
        pass
