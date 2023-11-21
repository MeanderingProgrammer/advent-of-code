from dataclasses import dataclass
from typing import Callable

from language.language import Language
from pojo.day import Day


@dataclass(frozen=True)
class LanguageStrategy:
    name: str
    languages: list[Language]

    def get(self, day: Day) -> list[Language]:
        templates: dict[str, Callable[[list[Language]], list[Language]]] = {
            "all": LanguageStrategy.__all,
            "fastest": LanguageStrategy.__fastest,
        }
        options = self.__with_solutions(day)
        return templates[self.name](options)

    def __with_solutions(self, day: Day) -> list[Language]:
        return [
            language
            for language in self.languages
            if language.solution_path(day).is_file()
        ]

    @staticmethod
    def __all(options: list[Language]) -> list[Language]:
        return options

    @staticmethod
    def __fastest(options: list[Language]) -> list[Language]:
        speed_ranking: dict[str, int] = {
            "rust": 1,
            "golang": 2,
            "java": 3,
            "ocaml": 4,
            "python": 5,
        }
        return [sorted(options, key=lambda language: speed_ranking[language.name])[0]]
