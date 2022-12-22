import abc
import time
from pathlib import Path
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

    @property
    def suffix(self) -> str:
        return Path(self.solution_file).suffix

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
    
    def run(self, day: Day, is_test: bool) -> float:
        start = time.time()
        self._do_run(day, is_test)
        return time.time() - start

    @abc.abstractmethod
    def _do_run(self, day: Day, is_test: bool):
        pass

    @abc.abstractmethod
    def template_processing(self, day: Day):
        pass


class InterprettedLanguage(Language):

    def compile(self, day: Day):
         # Interpreted languages do not need to be compiled
        pass
