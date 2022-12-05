import abc
import time
from pojo.day import Day


class Language(abc.ABC):

    def __init__(self):
        self.__setup = False
    
    @property
    @abc.abstractmethod
    def name(self):
        pass
    
    def setup(self):
        if not self.__setup:
            self._run_setup()
        self.__setup = True
    
    @abc.abstractmethod
    def _run_setup(self):
        pass
    
    @abc.abstractmethod
    def compile(self):
        pass
    
    def run(self, day: Day) -> float:
        start = time.time()
        self._do_run(day)
        return time.time() - start

    @abc.abstractmethod
    def _do_run(self, day: Day):
        pass


class InterprettedLanguage(Language):

    def compile(self):
         # Interpreted languages do not need to be compiled
        pass
