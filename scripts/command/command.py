import abc


class Command(abc.ABC):
    @abc.abstractmethod
    def info(self) -> dict:
        pass

    @abc.abstractmethod
    def run(self) -> None:
        pass
