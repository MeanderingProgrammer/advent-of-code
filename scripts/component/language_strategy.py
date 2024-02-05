from dataclasses import dataclass
from enum import StrEnum, auto

from language.language import Language
from pojo.day import Day


class StrategyName(StrEnum):
    ALL = auto()
    FASTEST = auto()


@dataclass(frozen=True)
class LanguageStrategy:
    name: StrategyName
    languages: list[Language]

    def get(self, day: Day) -> list[Language]:
        options = [
            language
            for language in self.languages
            if language.solution_path(day).is_file()
        ]
        if self.name == StrategyName.ALL:
            return options
        elif self.name == StrategyName.FASTEST:
            speed: dict[str, int] = dict(go=1, rust=2, java=3, ocaml=4, python=5, ts=6)
            ordered = sorted(options, key=lambda language: speed[language.name])
            return [ordered[0]]
        else:
            raise Exception(f"Unhandled name: {self.name}")
