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
        languages: list[Language] = []
        for language in self.languages:
            solution = day.file(language.file)
            if solution.is_file():
                languages.append(language)

        if self.name == StrategyName.ALL:
            return languages
        elif self.name == StrategyName.FASTEST:
            speed = dict(
                rust=1,
                go=2,
                zig=3,
                ocaml=4,
                elixir=5,
                python=6,
                ts=7,
                java=8,
            )
            ordered = sorted(languages, key=lambda language: speed[language.name])
            return [] if len(ordered) == 0 else [ordered[0]]
        else:
            raise Exception(f"Unhandled name: {self.name}")
