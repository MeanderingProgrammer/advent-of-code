import abc


class Language(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def solution_file(self) -> str:
        pass

    @abc.abstractmethod
    def additional_processing(self, year: str, day: str):
        pass
