import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from component.display_runtimes import Displayer
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


@dataclass(frozen=True)
class Runner:

    days: List[Day]
    languages: List[Language]
    run_args: List[str]

    def run(self):
        runtimes = self.__get_runtimes()
        Displayer(runtimes).display()

    def __get_runtimes(self) -> List[RuntimeInfo]:
        runtimes = []
        for day in self.days:
            os.chdir(f'{day.year}/{day.day}')
            runtimes.extend(self.__run_day(day))
            # Change back out of day directory
            os.chdir('../..')
        return runtimes

    def __run_day(self, day: Day) -> List[RuntimeInfo]:
        runtimes = []
        for language in self.__available_languages():
            runtime = self.__run_language(language, day)
            runtimes.append(runtime)
        return runtimes

    def __available_languages(self) -> List[Language]:
        return [
            language
            for language in self.languages
            if Path(language.solution_file).is_file()
        ]

    def __run_language(self, language: Language, day: Day) -> RuntimeInfo:
        print(f'Running year {day.year} day {day.day} with {language.name}')
        language.initial_setup()
        language.compile(day)
        runtime = language.run(day, self.run_args)
        print(f'Runtime: {runtime}')
        return RuntimeInfo(day, language.name, runtime)
