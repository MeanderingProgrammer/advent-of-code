import os
from pathlib import Path
from typing import List

from component.display_runtimes import Displayer
from component.language_factory import LanguageFactory
from language.language import Language
from pojo.day import Day
from pojo.runtime_info import RuntimeInfo


class Runner:

    def __init__(self, days: List[Day], run_args: List[str]):
        self.__factory = LanguageFactory()
        self.__days = days
        self.__run_args = run_args

    def run(self):
        runtimes = self.__get_runtimes()
        Displayer(runtimes).display()

    def __get_runtimes(self) -> List[RuntimeInfo]:
        runtimes = []
        for day in self.__days:
            os.chdir(f'{day.year}/{day.day}')
            runtimes.extend(self.__run_day(day))
            # Change back out of day directory
            os.chdir('../..')
        return runtimes

    def __run_day(self, day: Day) -> List[RuntimeInfo]:
        def is_solution(file_path):
            return file_path.is_file() and file_path.stem.lower() == 'solver'
        solution_files = [file_path for file_path in Path('.').iterdir() if is_solution(file_path)]

        runtimes = []
        for solution_file in solution_files:
            language = self.__factory.get_by_suffix(solution_file)
            runtime = self.__run_language(language, day)
            runtimes.append(runtime)
        return runtimes

    def __run_language(self, language: Language, day: Day) -> RuntimeInfo:
        print(f'Running year {day.year} day {day.day} with {language.name}')
        language.initial_setup()
        language.compile(day)
        runtime = language.run(day, self.__run_args)
        print(f'Runtime: {runtime}')
        return RuntimeInfo(day, language.name, runtime)
