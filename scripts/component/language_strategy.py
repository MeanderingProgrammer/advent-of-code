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
            speed = dict(rust=1, go=2, zig=3, java=4, ocaml=5, python=6, ts=7)
            ordered = sorted(options, key=lambda language: speed[language.name])
            return [ordered[0]]
        else:
            raise Exception(f"Unhandled name: {self.name}")
