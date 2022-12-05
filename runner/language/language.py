import abc
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
    
    @abc.abstractmethod
    def run(self, day: Day):
        pass
