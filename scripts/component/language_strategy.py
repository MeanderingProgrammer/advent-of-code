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
            solution = day.dir() / language.file
            if solution.is_file():
                languages.append(language)

        match self.name:
            case StrategyName.ALL:
                return languages
            case StrategyName.FASTEST:
                speed = dict(
                    rust=1,
                    go=2,
                    zig=3,
                    ocaml=4,
                    python=5,
                    elixir=6,
                    ts=7,
                    java=8,
                )
                ordered = sorted(languages, key=lambda language: speed[language.name])
                return [] if len(ordered) == 0 else [ordered[0]]
